from transformers import pipeline
import openai

openai.api_key = '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'


def generate_text(prompt, max_length=150):
    response = openai.Completion.create(
        engine="gpt-4",
        prompt=prompt,
        max_tokens=max_length,
        n=1,
        stop=None,
        temperature=1.0,
    )
    return response.choices[0].text.strip()