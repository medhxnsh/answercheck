import ollama
import json
import re
from sentence_transformers import SentenceTransformer, util

_model = None


def get_similarity_model():
    global _model
    if _model is None:
        _model = SentenceTransformer('all-MiniLM-L6-v2')
    return _model


def compute_similarity(student_answer: str, key_answer: str) -> float:
    model = get_similarity_model()
    embeddings = model.encode([student_answer, key_answer])
    score = util.cos_sim(embeddings[0], embeddings[1])
    return float(score)


def compute_marks(similarity: float, max_marks: int,
                  strictness: float) -> int:
    threshold = 0.65 + (strictness * 0.25)
    if similarity >= threshold:
        return max_marks
    elif similarity >= threshold - 0.15:
        return round(max_marks * 0.6)
    elif similarity >= 0.40:
        return round(max_marks * 0.3)
    return 0


def grade_answer(
    student_answer: str,
    key_answer: str,
    max_marks: int,
    strictness: float = 0.5
) -> dict:
    similarity = compute_similarity(student_answer, key_answer)
    estimated_marks = compute_marks(similarity, max_marks, strictness)

    prompt = f"""
You are a strict exam grader. You have ONLY two sources of truth:
1. The answer key provided below
2. The student's extracted answer

DO NOT use any outside knowledge to fill gaps.
DO NOT give marks for something correct but not in the answer key.
DO NOT penalize for something the answer key did not mention.
DO NOT reward additional correct info not present in the key.

ANSWER KEY: {key_answer}
STUDENT ANSWER: {student_answer}
SIMILARITY SCORE: {similarity:.3f}
ESTIMATED MARKS: {estimated_marks}
MAX MARKS: {max_marks}
STRICTNESS: {strictness}

Return JSON only, no text outside JSON:
{{"marks": int, "confidence": float, "justification": "string"}}
"""
    response = ollama.chat(
        model='mistral',
        messages=[{'role': 'user', 'content': prompt}]
    )

    content = response['message']['content']
    json_match = re.search(r'\{.*\}', content, re.DOTALL)
    if json_match:
        try:
            result = json.loads(json_match.group())
            result['similarity'] = similarity
            return result
        except json.JSONDecodeError:
            pass

    return {
        'marks': estimated_marks,
        'confidence': similarity,
        'justification': 'Graded by similarity score',
        'similarity': similarity
    }
