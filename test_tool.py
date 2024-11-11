from llm_tool_pattern_starter import ToolAgent,search_hackernews, process_data, fetch_weather,tool,add


# Basic testing
def test_tool_creation():
    assert hasattr(add, 'tool_definition'), "Tool decorator should add tool_definition"

# 测试 ToolAgent 的基本加法工具调用
def test_basic_addition():
    agent = ToolAgent([add])
    response = agent.run("Add 5 and 3")
    assert "8" in response, "Basic addition should work"

# 测试 ToolAgent 的错误处理
def test_error_handling():
    agent = ToolAgent([add])
    response = agent.run("Add invalid inputs")
    assert any(word in response.lower() for word in ["error", "sorry", "suggestions"]),"Should handle invalid inputs gracefully"

# 测试 search_hackernews 工具
def test_search_hackernews():
    agent = ToolAgent([search_hackernews])
    response = agent.run("Search articles about OpenAI")
    assert response, "HackerNews search should return results"

# 测试 process_data 工具
def test_process_data():
    data = [{"score": 10}, {"score": 20}, {"score": 30}]
    result = process_data(data, "average")
    assert result["average_score"] == 20, "Average score calculation should be correct"

# 测试 fetch_weather 工具
def test_fetch_weather():
    city = "Arlington"
    weather_data = fetch_weather(city)
    assert "temperature" in weather_data, "Weather data should include temperature"
