import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

class LLM:
    def __init__(self):
        self.client = None
        self._authenticate()
    
    def _authenticate(self):
        try:
            self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        except Exception as e:
            raise Exception(f"Error authenticating to OpenAI: {e}")
    
    def generate(self, user_prompt, system_prompt):
        try:
            if self.client:
                response = self.client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_prompt}
                    ]
                )
                return response.choices[0].message.content
        except Exception as e:
            raise Exception(f"Error generating response: {e}")