import os
import base64
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


def extract_math(image_path: str, answer_text: str) -> str:
    client = get_client()
    img_data = image_to_base64(image_path)

    response = client.chat.completions.create(
        model="meta-llama/llama-4-scout-17b-16e-instruct",
        messages=[{
            "role": "user",
            "content": [
                {
                    "type": "image_url",
                    "image_url": {"url": f"data:image/jpeg;base64,{img_data}"}
                },
                {
                    "type": "text",
                    "text": f"""The student wrote: "{answer_text}"
Extract all mathematical expressions and convert to LaTeX.
Return ONLY the LaTeX string. If no math, return the original text."""
                }
            ]
        }],
        max_tokens=512
    )
    return response.choices[0].message.content.strip()


def extract_diagram(image_path: str) -> str:
    client = get_client()
    img_data = image_to_base64(image_path)

    response = client.chat.completions.create(
        model="meta-llama/llama-4-scout-17b-16e-instruct",
        messages=[{
            "role": "user",
            "content": [
                {
                    "type": "image_url",
                    "image_url": {"url": f"data:image/jpeg;base64,{img_data}"}
                },
                {
                    "type": "text",
                    "text": "Describe this diagram from an exam answer. Focus on labels, arrows, and relationships shown. Return only the description."
                }
            ]
        }],
        max_tokens=512
    )
    return response.choices[0].message.content.strip()
