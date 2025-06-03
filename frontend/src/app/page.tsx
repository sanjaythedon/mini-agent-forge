"use client";

import { useState, useEffect, useRef } from "react";

export default function Home() {
  const [prompt, setPrompt] = useState("");
  const [selectedTool, setSelectedTool] = useState("web-search");
  const [userPrompt, setUserPrompt] = useState("");
  const [response, setResponse] = useState("");
  const [isStreaming, setIsStreaming] = useState(false);
  const wsRef = useRef<WebSocket | null>(null);

  useEffect(() => {
    // Initialize WebSocket connection
    const setupWebSocket = () => {
      const ws = new WebSocket('ws://localhost:8000/ws');
      
      ws.onopen = () => {
        console.log('WebSocket connection established');
      };
      
      ws.onmessage = (event) => {
        console.log('WebSocket message received:', event.data);
        const data = event.data;
        
        // Handle streaming response - append to the current response
        setResponse(prev => prev + data);
      };
      
      ws.onclose = () => {
        console.log('WebSocket connection closed');
        setIsStreaming(false);
        // Attempt to reconnect after a delay
        setTimeout(setupWebSocket, 3000);
      };
      
      ws.onerror = (error) => {
        console.error('WebSocket error:', error);
        setIsStreaming(false);
        ws.close();
      };
      
      wsRef.current = ws;
    };
    
    setupWebSocket();
    
    // Clean up the WebSocket connection when the component unmounts
    return () => {
      if (wsRef.current) {
        wsRef.current.close();
      }
    };
  }, []);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!prompt.trim() || isStreaming) return;

    // Store the user prompt
    setUserPrompt(prompt);
    
    // Clear previous response
    setResponse("");
    
    // Send the message to the WebSocket server
    if (wsRef.current && wsRef.current.readyState === WebSocket.OPEN) {
      setIsStreaming(true);
      
      wsRef.current.send(JSON.stringify({
        prompt: prompt,
        tool: selectedTool
      }));
      
      setPrompt("");
    } else {
      // WebSocket is not connected, show an error message
      setResponse("Error: Could not connect to the server. Please try again later.");
    }
  };

  return (
    <div className="flex flex-col min-h-screen bg-gray-50 dark:bg-gray-900">
      <header className="py-4 px-6 border-b bg-white dark:bg-gray-800">
        <h1 className="text-xl font-bold text-center">Chatbot</h1>
      </header>
      <div className="flex-1 overflow-auto p-4 space-y-4">
        {!userPrompt ? (
          <div className="flex items-center justify-center h-full">
            <p className="text-gray-500 dark:text-gray-400">Start a conversation...</p>
          </div>
        ) : (
          <>
            {/* User prompt */}
            <div className="flex justify-end">
              <div className="max-w-[80%] p-3 rounded-lg bg-blue-500 text-white">
                {userPrompt}
              </div>
            </div>
            
            {/* AI response */}
            {(response || isStreaming) && (
              <div className="flex justify-start">
                <div className="max-w-[80%] p-3 rounded-lg bg-gray-200 dark:bg-gray-700 text-gray-900 dark:text-gray-100">
                  {response}
                  {isStreaming && response.length === 0 && (
                    <span className="animate-pulse">•••</span>
                  )}
                </div>
              </div>
            )}
          </>
        )}
      </div>
      <div className="border-t bg-white dark:bg-gray-800 p-4">
        <form onSubmit={handleSubmit} className="flex gap-2">
          <input
            type="text"
            value={prompt}
            onChange={(e) => setPrompt(e.target.value)}
            placeholder="Type your message..."
            className="flex-1 px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 dark:bg-gray-700 dark:border-gray-600 dark:text-white"
            disabled={isStreaming}
          />
          <select
            value={selectedTool}
            onChange={(e) => setSelectedTool(e.target.value)}
            className="px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 dark:bg-gray-700 dark:border-gray-600 dark:text-white"
            disabled={isStreaming}
          >
            <option value="web-search">Web search</option>
            <option value="calculator">Calculator</option>
          </select>
          <button
            type="submit"
            className={`px-4 py-2 text-white rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 ${isStreaming ? 'bg-gray-400 cursor-not-allowed' : 'bg-blue-500 hover:bg-blue-600'}`}
            disabled={isStreaming}
          >
            {isStreaming ? 'Processing...' : 'Run'}
          </button>
        </form>
        {isStreaming && (
          <div className="mt-2 text-center text-sm text-gray-500">
            Streaming response from server...
          </div>
        )}
      </div>
    </div>
  );
}
