from abc import ABC, abstractmethod


class Tool(ABC):
    def __init__(self, tool_object):
        self.tool_object = tool_object

    @abstractmethod
    def execute(self, user_prompt):
        pass

    @staticmethod
    def generate_prompt():
        pass

class CalculatorTool(Tool):
    def __init__(self, tool_object):
        super().__init__(tool_object)

    def execute(self, user_prompt):
        return self.tool_object.calculate(user_prompt)

    @staticmethod
    def generate_prompt():
        prompt = """
        You are a friendly assistant who helps with calculations. Present the user's calculation query along with its result in a clear, conversational way. 
            
        IMPORTANT: 
        - Use plain text with standard math operators (+, -, *, /, ^, etc.)
        - DO NOT use any LaTeX math delimiters (like $ or $$)
        - DO NOT use markdown formatting
        - Keep the response concise but warm
        - Only use the information provided in the user's query and the calculation result
        """
        return prompt

class WebSearchTool(Tool):
    def __init__(self, tool_object):
        super().__init__(tool_object)

    def execute(self, user_prompt):
        return self.tool_object.search(user_prompt)

    @staticmethod
    def generate_prompt():
        prompt = """
        You are a helpful assistant who provides web search results. Generate an HTML-formatted response that lists all search results with proper styling.

        Format your response as follows:
        1. Start with a header element containing a friendly reply for the search query
        2. Create a numbered list of results where each item contains:
        - The title in bold
        - The URL as a clickable link
        3. End with a closing remark in a paragraph

        Example format:
        <header><h2>Some friendly reply about the query:</h2></header>
        <ol>
            <li><strong>Result 1 Title</strong><a href="https://example.com">https://example.com</a></li>
            <li><strong>Result 2 Title</strong><a href="https://example.com">https://example.com</a></li>
            <li><strong>Result 3 Title</strong><a href="https://example.com">https://example.com</a></li>
        </ol>
        <footer><p>Some closing remark about the search results</p></footer>
        """
        return prompt
    