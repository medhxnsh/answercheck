import os
import base64
import json
import re
from groq import Groq

_client = None


def get_client():
    global _client
    if _client is None:
        _client = Groq(api_key=os.environ['GROQ_API_KEY'])
    return _client


def image_to_base64(image_path: str) -> str:
    with open(image_path, 'rb') as f:
        return base64.b64encode(f.read()).decode()


def segment_questions(image_path: str) -> dict:
    client = get_client()
    img_data = image_to_base64(image_path)

    response = client.chat.completions.create(
        model="meta-llama/llama-4-scout-17b-16e-instruct",
        messages=[{
            "role": "user",
            "content": [
                {
                    "type": "image_url",
                    "image_url": {
                        "url": f"data:image/jpeg;base64,{img_data}"
                    }
                },
                {
                    "type": "text",
                    "text": """Read this handwritten answer sheet carefully.
Find every question and its answer.
Questions labeled Q1/Q2/Q3 or 1./2./3.
Answers labeled Ans1/Ans2/Ans3 or written below each question.
Also detect if answer contains math equations (has_math)
or diagrams/drawings (has_diagram).

Return ONLY valid JSON:
{
  "questions": [
    {
      "number": 1,
      "answer_text": "exact answer text",
      "has_math": false,
      "has_diagram": false
    }
  ]
}"""
                }
            ]
        }],
        max_tokens=2048
    )

    content = response.choices[0].message.content
    json_match = re.search(r'\{.*\}', content, re.DOTALL)
    if json_match:
        try:
            return json.loads(json_match.group())
        except json.JSONDecodeError:
            return {"questions": []}
    return {"questions": []}
