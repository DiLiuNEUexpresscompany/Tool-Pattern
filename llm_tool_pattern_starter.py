import json
import re
import requests
import os
from typing import List, Dict
from dotenv import load_dotenv 
from groq import Groq

# Loading environment variables in .env files
load_dotenv()

# XML parsing utility to handle tool calls
def parse_tool_call(tool_call_str: str):
    """Parse tool calls from XML format."""
    pattern = r'</?tool_call>'
    clean_tags = re.sub(pattern, '', tool_call_str)
    try:
        return json.loads(clean_tags)
    except:
        return None

TOOL_SYSTEM_PROMPT = """
You are a function-calling AI model. You are provided with function signatures 
within <tools></tools> XML tags.  
You may call one or more functions to assist with the user query. Don't make 
assumptions about what values to plug into functions. 
For each function call return a json object with function name and arguments 
within <tool_call></tool_call> XML tags as follows:

<tool_call> 
{{"name": "<function-name>", "arguments": <args-dict>}} 
</tool_call>

Here are the available tools:

<tools> 
{tools} 
</tools>
"""

# Tool decorator to attach metadata to functions
def tool(func):
    """Tool decorator to register function as a tool."""
    func.tool_definition = {
        "name": func.__name__,
        "description": func.__doc__,
        "parameters": getattr(func, 'parameters', {}),
        "returns": getattr(func, 'returns', {})
    }
    return func

# ToolAgent to handle the execution of tools
class ToolAgent:
    def __init__(self, tools):
        self.tools = tools
        # Get Groq API key from environment variable
        api_key = os.getenv("GROQ_API_KEY")
        self.client = Groq(api_key=api_key)
        self.model = "llama3-groq-70b-8192-tool-use-preview"  # Specify the model name

    def run(self, user_msg: str) -> str:
        # Prepare system prompt including tool definitions
        tools_definitions = '\n'.join([json.dumps(tool.tool_definition) for tool in self.tools])
        system_prompt = TOOL_SYSTEM_PROMPT.format(tools=tools_definitions)

        # Create a message list for the conversation
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_msg}
        ]

        # Send the message to the language model and get a response
        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages
        )

        # Access the assistant's reply content correctly from the response object
        assistant_reply = response.choices[0].message.content

        # Parse the assistant's response to check for any tool calls
        tool_call = parse_tool_call(assistant_reply)
        if tool_call:
            func_name = tool_call.get("name")
            arguments = tool_call.get("arguments", {})

            # Map LLM-provided argument names to match the tool's expected parameters
            if func_name == "add":
                arguments = {"x": arguments.get("num1"), "y": arguments.get("num2")}

            for tool in self.tools:
                if tool.__name__ == func_name:
                    try:
                        result = tool(**arguments)
                        # Send tool execution result back to the model to generate the final answer
                        messages.append({"role": "assistant", "content": assistant_reply})
                        messages.append({"role": "user", "content": f"The result of {func_name} is: {json.dumps(result)}"})
                        final_response = self.client.chat.completions.create(
                            model=self.model,
                            messages=messages
                        )
                        return final_response.choices[0].message.content
                    except Exception as e:
                        return json.dumps({"error": str(e)})
        else:
            # If no tool call, return the assistant's reply directly
            return assistant_reply


# Tool Implementations

# 1. API Interaction Tool: HackerNews Search
@tool
def search_hackernews(query: str, limit: int = 5) -> List[Dict]:
    """Search HackerNews articles by keyword."""
    url = f"http://hn.algolia.com/api/v1/search?query={query}&numericFilters=points>10"
    try:
        response = requests.get(url)
        response.raise_for_status()
        results = response.json()['hits'][:limit]
        return [{'title': item['title'], 'url': item['url'], 'score': item['points']} for item in results if item.get('url')]
    except Exception as e:
        return [{"error": f"Failed to fetch articles: {str(e)}"}]

# 2. Data Processing Tool: Sum Values
@tool
def process_data(data: List[Dict], operation: str = "count") -> Dict:
    """
    Process a list of articles with basic operations.

    Args:
        data (List[Dict]): List of articles to process
        operation (str): Operation to perform (count, average, max)

    Returns:
        Dict: Results of the operation
    """
    if operation == "count":
        return {"count": len(data)}
    elif operation == "average":
        # Calculate average score if 'score' is present in data
        scores = [article.get("score", 0) for article in data if "score" in article]
        return {"average_score": sum(scores) / len(scores) if scores else 0}
    elif operation == "max":
        # Find article with max score
        max_article = max(data, key=lambda x: x.get("score", 0), default=None)
        return {"max_score_article": max_article} if max_article else {}
    else:
        return {"error": "Invalid operation"}

# 3. External Service Integration Tool: Fetch Weather
@tool
def fetch_weather(city: str, units: str = "metric") -> Dict:
    """
    Fetch the current weather for a specified city.

    Args:
        city (str): City name to fetch the weather for.
        units (str): Units of measurement (metric, imperial).

    Returns:
        Dict: Weather details for the city.
    """
    api_key = os.getenv("WEATHER_API_KEY")  # 从环境变量中获取天气 API 密钥
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&units={units}&appid={api_key}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        return {
            "city": data.get("name"),
            "temperature": data["main"].get("temp"),
            "weather": data["weather"][0].get("description"),
            "humidity": data["main"].get("humidity"),
            "wind_speed": data["wind"].get("speed")
        }
    except Exception as e:
        return {"error": f"Failed to fetch weather data: {str(e)}"}
@tool
def add(x: int, y: int) -> int:
    """Add two numbers."""
    return x + y