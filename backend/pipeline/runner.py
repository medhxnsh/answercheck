from .preprocessor import preprocess_image, save_preprocessed
from .segmenter import segment_questions
from .classifier import classify_answer
from .ocr import extract_text_ocr
from .extractor import extract_math, extract_diagram
from .grader import grade_answer
import cv2
import tempfile
import os


def run_pipeline(
    image_path: str,
    answer_key: list,
    strictness: float = 0.5
) -> list:
    """Orchestrate the full grading pipeline for one submission.

    Steps:
      1. Preprocess the image (denoise, deskew, threshold)
      2. Segment questions via LLaVA
      3. Classify each answer type
      4. Extract text (OCR / LLaVA math / LLaVA diagram)
      5. Grade against the answer key
    """
    preprocessed_path = image_path.replace('.jpg', '_processed.jpg')
    preprocessed_path = preprocessed_path.replace('.png', '_processed.png')
    save_preprocessed(image_path, preprocessed_path)

    segmented = segment_questions(preprocessed_path)
    questions = segmented.get('questions', [])

    results = []

    for question in questions:
        q_num = question.get('number')
        answer_text = question.get('answer_text', '')

        answer_type = classify_answer(question)

        if answer_type == 'text_only':
            extracted = answer_text
        elif answer_type == 'math_heavy':
            extracted = extract_math(preprocessed_path, answer_text)
        elif answer_type == 'diagram':
            extracted = extract_diagram(preprocessed_path)
        else:  # mixed
            extracted = answer_text

        key_entry = next(
            (k for k in answer_key if k.get('question_number') == q_num),
            None
        )

        if key_entry:
            grade = grade_answer(
                extracted,
                key_entry['expected_answer'],
                key_entry['max_marks'],
                strictness
            )
        else:
            grade = {
                'marks': 0,
                'confidence': 0,
                'justification': 'No answer key entry found',
                'similarity': 0
            }

        results.append({
            'question_number': q_num,
            'extracted_text': extracted,
            'answer_type': answer_type,
            'similarity_score': grade.get('similarity', 0),
            'ai_marks': grade.get('marks', 0),
            'ai_confidence': grade.get('confidence', 0),
            'ai_justification': grade.get('justification', '')
        })

    return results
