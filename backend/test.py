import unittest
import json
import os
from fastapi.testclient import TestClient
from fastapi import WebSocketDisconnect
from dotenv import load_dotenv
from api import app

# Load environment variables for test configuration
load_dotenv()

class TestWebSocket(unittest.TestCase):
    """Test cases for WebSocket endpoint."""
    
    @classmethod
    def setUpClass(cls):
        """Set up test client and test data before any tests run."""
        cls.client = TestClient(app)
        cls.valid_prompt = "who is virat kohli?"  # < 500 characters
        cls.invalid_prompt = """
        In a quiet village nestled between green hills and winding rivers, life moved at a gentle pace. The sun rose slowly over the rooftops, casting golden light on cobblestone streets. Children laughed as they ran past the bakery, where the scent of fresh bread filled the air. Elderly neighbors waved from porches, their faces lit with warmth. Evenings brought families together, sharing stories under starlit skies. Though simple, each day held its own quiet beauty—a reminder that peace often lives in the smallest moments.
        """  # > 500 characters
        cls.test_user = "test_user"
    
    
    def test_websocket_happy_path(self):
        """Test WebSocket with valid prompt (less than 500 characters)."""
        with self.client.websocket_connect("/ws") as websocket:
            # Send a valid prompt
            test_message = {
                "prompt": self.valid_prompt,
                "tool": "web-search"
            }
            websocket.send_text(json.dumps(test_message))
            
            # Verify response
            response = websocket.receive_text()
            response_data = json.loads(response)
            
            self.assertEqual(response_data["status"], "inprogress")
    
    def test_websocket_invalid_prompt_length(self):
        """Test WebSocket with invalid prompt (more than 500 characters)."""
        with self.client.websocket_connect("/ws") as websocket:
            # Send an invalid prompt (too long)
            test_message = {
                "prompt": self.invalid_prompt,
                "tool": "web-search"
            }
            websocket.send_text(json.dumps(test_message))
            
            # Verify error response
            response = websocket.receive_text()
            response_data = json.loads(response)
            
            self.assertEqual(response_data["status"], "error")
            self.assertEqual(response_data["message"], "Value error, Prompt must not exceed 500 words")

if __name__ == '__main__':
    unittest.main()
