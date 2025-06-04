"use client";

import { useState, useEffect, useRef } from "react";

interface ChatHistory {
  timestamp: string;
  prompt: string;
  tool: string;
  response: string;
}

export default function Home() {
  const [prompt, setPrompt] = useState("");
  const [selectedTool, setSelectedTool] = useState("web-search");
  const [isStreaming, setIsStreaming] = useState(false);
  const [chatHistory, setChatHistory] = useState<ChatHistory[]>([]);
  const wsRef = useRef<WebSocket | null>(null);
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const messagesContainerRef = useRef<HTMLDivElement>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  // Fetch chat history on component mount
  useEffect(() => {
    const fetchChatHistory = async () => {
      try {
        const response = await fetch('http://127.0.0.1:8000/get');
        if (!response.ok) {
          throw new Error('Failed to fetch chat history');
        }
        const data = await response.json();
        setChatHistory(data.user_prompts || []);
      } catch (error) {
        console.error('Error fetching chat history:', error);
      } finally {
        // Scroll to bottom after loading history
        setTimeout(scrollToBottom, 100);
      }
    };
    
    fetchChatHistory();
  }, []);

  // Scroll to bottom when chat history or streaming state changes
  useEffect(() => {
    // Use requestAnimationFrame to ensure the DOM has updated
    const timer = setTimeout(() => {
      scrollToBottom();
    }, 0);
    return () => clearTimeout(timer);
  }, [chatHistory, isStreaming]);

  useEffect(() => {
    // Initialize WebSocket connection
    const setupWebSocket = () => {
      const ws = new WebSocket('ws://localhost:8000/ws');
      
      ws.onopen = () => {
        console.log('WebSocket connection established');
      };
      
      ws.onmessage = (event) => {
        console.log('WebSocket message received:', event.data);
        const data = JSON.parse(event.data);
        if (data.status && data.status === 'complete') {
          setIsStreaming(false);
          return;
        }
        
        // Update the last chat entry's response with the streaming data
        setChatHistory(prev => {
          const newHistory = [...prev];
          const lastIndex = newHistory.length - 1;
          if (lastIndex >= 0) {
            newHistory[lastIndex] = {
              ...newHistory[lastIndex],
              response: (newHistory[lastIndex].response || '') + data.chunk
            };
          }
          return newHistory;
        });
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

    // Create a new chat history entry
    const newEntry: ChatHistory = {
      timestamp: new Date().toISOString(),
      prompt: prompt,
      tool: selectedTool,
      response: ""
    };
    
    setChatHistory(prev => [...prev, newEntry]);
    
    // Send the message to the WebSocket server
    if (wsRef.current && wsRef.current.readyState === WebSocket.OPEN) {
      setIsStreaming(true);
      
      wsRef.current.send(JSON.stringify({
        prompt: prompt,
        tool: selectedTool
      }));
      
      setPrompt("")
    } else {
      // WebSocket is not connected, show an error message
      setChatHistory(prev => {
        const newHistory = [...prev];
        const lastIndex = newHistory.length - 1;
        if (lastIndex >= 0) {
          newHistory[lastIndex] = {
            ...newHistory[lastIndex],
            response: "Error: Could not connect to the server. Please try again later."
          };
        }
        return newHistory;
      });
    }
  };

  return (
    <div className="flex flex-col h-screen bg-gray-50 dark:bg-gray-900">
      <header className="shrink-0 py-4 px-6 border-b bg-white dark:bg-gray-800">
        <h1 className="text-xl font-bold text-center">Chatbot</h1>
      </header>
      <div className="flex-1 overflow-hidden flex flex-col">
        <div className="flex-1 overflow-y-auto p-4 space-y-4" ref={messagesContainerRef}>
          {chatHistory.length === 0 ? (
            <div className="flex items-center justify-center h-full">
              <p className="text-gray-500 dark:text-gray-400">Start a conversation...</p>
            </div>
          ) : (
            chatHistory.map((chat, index) => (
              <div key={index} className="space-y-2">
                <div className="flex justify-end">
                  <div className="max-w-[80%] p-3 rounded-lg bg-blue-500 text-white">
                    {chat.prompt}
                  </div>
                </div>
                <div className="flex justify-start">
                  <div 
                    className="max-w-[80%] p-3 rounded-lg bg-gray-200 dark:bg-gray-700 text-gray-900 dark:text-gray-100 [&_a]:text-blue-600 [&_a]:dark:text-blue-400 [&_a]:underline [&_a]:break-all [&_strong]:font-bold"
                    dangerouslySetInnerHTML={{ __html: chat.response || (index === chatHistory.length - 1 && isStreaming ? '•••' : '') }}
                  />
                </div>
              </div>
            ))
          )}
          <div ref={messagesEndRef} />
        </div>
        <div className="shrink-0 border-t bg-white dark:bg-gray-800 p-4">
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
        </div>
      </div>
    </div>
  );
}
