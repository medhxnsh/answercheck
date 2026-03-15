from pipeline.runner import run_pipeline

answer_key = [
    {
        "question_number": 1,
        "expected_answer": "Asiatic lion is found only in the Gir forest sanctuary in Gujarat",
        "max_marks": 5
    },
    {
        "question_number": 2,
        "expected_answer": "The great Indian hornbills eat fruits such as figs but also hunt insects and lizards",
        "max_marks": 5
    },
    {
        "question_number": 3,
        "expected_answer": "The great Indian hornbill are at risk because the forests where they live are being cut down or destroyed and they are also hunted by many people for their beaks",
        "max_marks": 5
    }
]

results = run_pipeline(
    image_path="test_sheet.jpg",
    answer_key=answer_key,
    strictness=0.5
)

if not results:
    print("❌ No questions detected — image or segmenter issue")
else:
    for r in results:
        print(f"\nQ{r['question_number']}")
        print(f"  Type:      {r['answer_type']}")
        print(f"  Extracted: {r['extracted_text'][:100]}")
        print(f"  Marks:     {r['ai_marks']}")
        print(f"  Similarity:{r['similarity_score']:.3f}")
        print(f"  Reason:    {r['ai_justification'][:100]}")
