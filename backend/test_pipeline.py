from paddleocr import PaddleOCR
import ollama
from sentence_transformers import SentenceTransformer, util

# Test 1 — PaddleOCR
print("\n--- Test 1: PaddleOCR ---")
ocr = PaddleOCR(use_angle_cls=True, lang='en')
result = ocr.ocr('../test_handwriting.jpg')
print("PaddleOCR:", result)

# Test 2 — LLaVA
print("\n--- Test 2: LLaVA ---")
response = ollama.chat(
    model='llava',
    messages=[{
        'role': 'user',
        'content': 'What handwritten text do you see in this image?',
        'images': ['../test_handwriting.jpg']
    }]
)
print("LLaVA:", response['message']['content'])

# Test 3 — Mistral
print("\n--- Test 3: Mistral ---")
response = ollama.chat(
    model='mistral',
    messages=[{'role': 'user', 'content': 'Reply with OK if you are working.'}]
)
print("Mistral:", response['message']['content'])

# Test 4 — Sentence Transformers
print("\n--- Test 4: Sentence Transformers ---")
model = SentenceTransformer('all-MiniLM-L6-v2')
score = util.cos_sim(
    model.encode("Newton's third law: every action has an equal and opposite reaction"),
    model.encode("For every action there is an equal and opposite reaction")
)
print("Similarity score (should be > 0.85):", float(score))

print("\n✅ All tests complete")
