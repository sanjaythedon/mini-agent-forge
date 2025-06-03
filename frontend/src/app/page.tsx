"use client";

import { useState } from "react";

export default function Home() {
  const [prompt, setPrompt] = useState("");
  const [selectedTool, setSelectedTool] = useState("Web search");
  const [messages, setMessages] = useState<{ role: string; content: string }[]>([]);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!prompt.trim()) return;

    // Add user message to chat
    setMessages([...messages, { role: "user", content: prompt }]);
    
    // Here you would normally make an API call to process the prompt with the selected tool
    // For now, we'll just add a placeholder response
    setMessages(prev => [
      ...prev, 
      { 
        role: "assistant", 
        content: `Processed "${prompt}" using ${selectedTool} tool` 
      }
    ]);
    
    // Clear the prompt
    setPrompt("");
  };

  return (
    <div className="flex flex-col min-h-screen bg-gray-50 dark:bg-gray-900">
      {/* Header */}
      <header className="py-4 px-6 border-b bg-white dark:bg-gray-800">
        <h1 className="text-xl font-bold text-center">Chatbot</h1>
      </header>

      {/* Chat area */}
      <div className="flex-1 overflow-auto p-4 space-y-4">
        {messages.length === 0 ? (
          <div className="flex items-center justify-center h-full">
            <p className="text-gray-500 dark:text-gray-400">Start a conversation...</p>
          </div>
        ) : (
          messages.map((message, index) => (
            <div 
              key={index} 
              className={`flex ${message.role === "user" ? "justify-end" : "justify-start"}`}
            >
              <div 
                className={`max-w-[80%] p-3 rounded-lg ${
                  message.role === "user" 
                    ? "bg-blue-500 text-white" 
                    : "bg-gray-200 dark:bg-gray-700 text-gray-900 dark:text-gray-100"
                }`}
              >
                {message.content}
              </div>
            </div>
          ))
        )}
      </div>

      {/* Input area */}
      <div className="border-t bg-white dark:bg-gray-800 p-4">
        <form onSubmit={handleSubmit} className="flex gap-2">
          <input
            type="text"
            value={prompt}
            onChange={(e) => setPrompt(e.target.value)}
            placeholder="Type your message..."
            className="flex-1 px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 dark:bg-gray-700 dark:border-gray-600 dark:text-white"
          />
          
          <select
            value={selectedTool}
            onChange={(e) => setSelectedTool(e.target.value)}
            className="px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 dark:bg-gray-700 dark:border-gray-600 dark:text-white"
          >
            <option value="Web search">Web search</option>
            <option value="Calculator">Calculator</option>
          </select>
          
          <button
            type="submit"
            className="px-4 py-2 bg-blue-500 text-white rounded-lg hover:bg-blue-600 focus:outline-none focus:ring-2 focus:ring-blue-500"
          >
            Run
          </button>
        </form>
      </div>
    </div>
  );
}
