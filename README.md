# LLM Tool Pattern Implementation Project

This project implements a tool pattern for Large Language Models (LLMs) to interact with external functions through structured prompts in XML format. The project includes various tool functions, such as basic arithmetic, string manipulation, and API interactions, allowing the LLM to perform tasks beyond its original training data.

## Table of Contents
- [Project Overview](#project-overview)
- [Features](#features)
- [Project Structure](#project-structure)
- [Installation](#installation)
- [Usage](#usage)
- [Examples](#examples)
- [Testing](#testing)
- [Environment Variables](#environment-variables)
- [Contributing](#contributing)
- [License](#license)

## Project Overview

This project is designed to:
- Allow an LLM to call external tools by parsing structured prompts in XML format.
- Use a `ToolAgent` class that registers multiple tools, processes user queries, and determines the correct tool to call based on the query.
- Enable the model to call tools through a predefined prompt structure and handle function calls that return JSON objects.

## Features

1. **Tool Registration**: Use a decorator to register tool functions for LLM access.
2. **LLM Interaction**: An LLM prompt structure to specify tool functions, parameters, and descriptions.
3. **API Interaction**: Implement example tools, including a HackerNews search API, weather fetching, and data processing.
4. **Error Handling**: Handle invalid inputs gracefully and return appropriate error messages.
5. **Testing**: Basic tests using `pytest` to verify tool functionality.

## Project Structure

```plaintext
.
├── example_tools.py            # Contains the implementation of example tools
├── test_tool.py                # Contains unit tests for tool functions
├── tool_agent.py               # Contains ToolAgent and helper functions
├── .env                        # Stores environment variables (API keys)
└── README.md                   # Project documentation
```

### Files

- **example_tools.py**: Implements various tool functions, such as `add`, `search_hackernews`, and `fetch_weather`.
- **test_tool.py**: Contains `pytest`-based tests for validating the functionality of each tool.
- **tool_agent.py**: Core class, `ToolAgent`, that handles tool registration, LLM query parsing, and tool execution.
- **.env**: Used to store sensitive information, like API keys.

## Installation

1. **Clone the repository**:

    ```bash
    git clone https://github.com/DiLiuNEUexpresscompany/Tool-Pattern
    cd LLM-Tool-Pattern-Project
    ```

2. **Install required packages**:

    Install Python dependencies listed in `requirements.txt`.

    ```bash
    pip install -r requirements.txt
    ```

3. **Set up environment variables**:

    Create a `.env` file in the project root and add your API keys as follows:

    ```plaintext
    GROQ_API_KEY="your_groq_api_key"
    WEATHER_API_KEY="your_weather_api_key"
    ```

## Usage

To run the project, you can use the provided `example_tools.py` script, which demonstrates different tool calls.

```bash
python example_tools.py
```

Alternatively, you can interact with specific tools through the `ToolAgent` class by creating your own queries.

### Example Usage

Here’s an example of how to use the `ToolAgent`:

```python
from tool_agent import ToolAgent
from example_tools import add, search_hackernews, fetch_weather

# Initialize ToolAgent with desired tools
agent = ToolAgent([add, search_hackernews, fetch_weather])

# Run a query with ToolAgent
response = agent.run("Add 5 and 3")
print(response)
```

## Examples

### Addition Tool
The `add` tool takes two integers and returns their sum.

```python
response = agent.run("Add 10 and 15")
# Expected output: {"result": 25}
```

### Weather Tool
Fetch the current weather for a specified city using the `fetch_weather` tool.

```python
response = agent.run("What is the weather in New York?")
# Expected output: JSON containing weather data for New York
```

### HackerNews Search Tool
Search for articles on HackerNews using keywords.

```python
response = agent.run("Search articles about AI")
# Expected output: List of articles with titles, URLs, and scores
```

## Testing

Tests are implemented in `test_tool.py` using `pytest`. To run the tests, simply execute:

```bash
pytest test_tool.py
```

The tests cover the following:
- Tool registration and functionality
- Valid input handling
- Error handling for invalid inputs

### Sample Tests

A sample test for addition:

```python
def test_basic_addition():
    agent = ToolAgent([add])
    response = agent.run("Add 5 and 3")
    assert "8" in response, "Basic addition should work"
```

## Environment Variables

This project requires a `.env` file to store sensitive information such as API keys. The required variables are:

- **GROQ_API_KEY**: Your API key for the Groq API.
- **WEATHER_API_KEY**: Your API key for the OpenWeather API.

### Example .env File

```plaintext
GROQ_API_KEY="your_groq_api_key"
WEATHER_API_KEY="your_weather_api_key"
```

## Contributing

We welcome contributions! Please fork the repository, make your changes, and submit a pull request.

## License

This project is licensed under the MIT License. See the LICENSE file for details.
