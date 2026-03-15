def classify_answer(question: dict) -> str:
    """Classify a segmented question as text_only, math_heavy, diagram, or mixed."""
    if question.get('has_diagram'):
        return 'diagram'
    if question.get('has_math'):
        if question.get('answer_text', '').strip():
            return 'mixed'
        return 'math_heavy'
    return 'text_only'
