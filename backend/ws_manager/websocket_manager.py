import asyncio
import json
from datetime import datetime
from typing import Dict, Any, AsyncGenerator
from fastapi import WebSocket
from models import Payload
from LLM.llm import LLM
from Database.operations import DatabaseOperations
from Database.connections.postgres import PostgresConnection
from Database.operations import DatabaseTableManager, DatabaseDataManager
from Redis.redis import Redis
from functions import generate_prompt_to_llm, ToolEnum
import os
from dotenv import load_dotenv
load_dotenv()

class WebSocketManager:
    def __init__(self, websocket: WebSocket):
        self.websocket = websocket
        self.llm = LLM()
        self.redis = Redis(
            host=os.getenv("REDIS_HOST"),
            port=os.getenv("REDIS_PORT"),
            db=os.getenv("REDIS_DB")
        )
        self.db_connection = PostgresConnection(
            host=os.getenv("POSTGRES_HOST"),
            port=os.getenv("POSTGRES_PORT"),
            user=os.getenv("POSTGRES_USER"),
            password=os.getenv("POSTGRES_PASSWORD"),
            database=os.getenv("POSTGRES_DB")
        )
        self._init_database()

    def _init_database(self):
        """Initialize database tables if they don't exist"""
        table_manager = DatabaseTableManager(self.db_connection)
        data_manager = DatabaseDataManager("%s", self.db_connection)
        self.db = DatabaseOperations(
            connection_manager=self.db_connection,
            table_manager=table_manager,
            data_manager=data_manager
        )
        
        columns = {
            "id": "SERIAL PRIMARY KEY",
            "timestamp": "TIMESTAMP",
            "prompt": "TEXT",
            "tool": "TEXT",
            "response": "TEXT"
        }
        self.db.create_table("prompt_log", columns)

    async def handle_connection(self):
        """Handle the WebSocket connection lifecycle"""
        await self.websocket.accept()
        try:
            await self._handle_messages()
        except asyncio.CancelledError:
            print("Client disconnected")
        except Exception as e:
            print(f"WebSocket connection error: {e}")
            await self._send_error(str(e))
        finally:
            await self._close_connection()

    async def _handle_messages(self):
        """Handle incoming WebSocket messages"""
        while True:
            try:
                data = await self.websocket.receive_json()
                await self._process_message(data)
            except asyncio.CancelledError:
                raise
            except Exception as e:
                print(f"Error in websocket: {e}")
                await self._send_error(str(e))

    async def _process_message(self, data: Dict[str, Any]):
        """Process a single WebSocket message"""
        try:
            # Validate payload using Pydantic model
            payload = Payload(**data)
            print(f"Received from client: {data}")

            # Generate response using LLM
            response = await self._generate_llm_response(payload.prompt, payload.tool)
            
            # Log the interaction
            await self._log_interaction(payload.prompt, payload.tool.value, response)
            
        except ValueError as e:
            # Send validation error to client
            for err in e.errors():
                error_msg = err['msg']
                print(f"Validation error: {error_msg}")
                await self._send_error(error_msg)
                return

    async def _generate_llm_response(self, user_prompt: str, tool: ToolEnum) -> str:
        """Generate response using LLM and stream it back to the client"""
        response_data = generate_prompt_to_llm(user_prompt, tool)
        results = response_data['results']
        system_prompt = response_data['system_prompt']
        prompt_to_llm = f"USER PROMPT:{user_prompt}\n\nResponse: {results}"
        
        response = ""
        try:
            response_generator = self.llm.generate_stream(prompt_to_llm, system_prompt)
            
            async for chunk in response_generator:
                if chunk:  # Only process non-empty chunks
                    response += chunk
                    await self._send_chunk(chunk)
                    await asyncio.sleep(0.001)
            
            print('Full response:')
            print(response)
            await self._send_complete()
            return response
            
        except Exception as e:
            error_msg = f"Error processing chunks: {e}"
            print(error_msg)
            await self._send_error(error_msg)
            raise

    async def _log_interaction(self, user_prompt: str, tool: str, response: str):
        """Log the interaction to database and Redis"""
        try:
            data = {
                "timestamp": datetime.now(),
                "prompt": user_prompt,
                "tool": tool,
                "response": response
            }
        
            # Log to PostgreSQL
            self.db.insert("prompt_log", data)
        
            # Update Redis
            data['timestamp'] = data['timestamp'].isoformat()
            self.redis.push("user", json.dumps(data))
            self.redis.trim("user", 0, 9)
        except Exception as e:
            print(f"Error logging interaction: {e}")
            await self._send_error(str(e))

    async def _send_chunk(self, chunk: str):
        """Send a chunk of the response to the client"""
        await self.websocket.send_json({"chunk": chunk, "status": "inprogress"})

    async def _send_complete(self):
        """Send completion status to the client"""
        await self.websocket.send_json({"status": "complete"})

    async def _send_error(self, error_msg: str):
        """Send error message to the client"""
        await self.websocket.send_json({"status": "error", "message": error_msg})

    async def _close_connection(self):
        """Safely close the WebSocket connection"""
        try:
            await self.websocket.close()
        except Exception as e:
            print(f"Error closing WebSocket: {e}")
