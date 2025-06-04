import os
from dotenv import load_dotenv
from openai import AsyncOpenAI

load_dotenv()

class LLM:
    def __init__(self):
        self.client = None
        self._authenticate()
    
    def _authenticate(self):
        try:
            self.client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        except Exception as e:
            raise Exception(f"Error authenticating to OpenAI: {e}")
    
    async def generate_stream(self, user_prompt, system_prompt):
        try:
            if not self.client:
                raise Exception("OpenAI client not initialized")
                
            stream = await self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                stream=True,
                timeout=30.0  
            )
            
            async for chunk in stream:
                if chunk.choices and chunk.choices[0].delta.content:
                    content = chunk.choices[0].delta.content
                    # print(content, end="", flush=True)
                    yield content
                        
        except Exception as e:
            print(f"Error in generate_stream: {e}")
            yield f"Error: {str(e)}"