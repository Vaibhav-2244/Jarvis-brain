from groq import Groq

MODEL_NAME = "llama-3.1-8b-instant"

class LLM:
    def __init__(self, api_key):
        self.client = Groq(api_key=api_key)

    def generate(self, messages):
        completion = self.client.chat.completions.create(
            model=MODEL_NAME,
            messages=messages,
            temperature=0.4,
            max_tokens=200
        )
        return completion.choices[0].message.content.strip()
