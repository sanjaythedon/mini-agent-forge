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
                # Create a streaming completion
                response = self.client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_prompt}
                    ],
                    stream=True  # Enable streaming
                )
                
                # Initialize an empty string to collect the full response
                full_response = ""
                
                # Process and print the streaming response
                for chunk in response:
                    # Extract the content from the chunk
                    if chunk.choices and chunk.choices[0].delta.content:
                        content = chunk.choices[0].delta.content
                        print(content, end="", flush=True)  # Print without newline and flush immediately
                        full_response += content
                
                print()  # Print a newline at the end
                return full_response
        except Exception as e:
            raise Exception(f"Error generating response: {e}")