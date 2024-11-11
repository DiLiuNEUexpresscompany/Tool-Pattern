from llm_tool_pattern_starter import ToolAgent,search_hackernews, process_data, fetch_weather
def main():
    agent = ToolAgent([search_hackernews, process_data, fetch_weather])

    user_input = "Please help me search for articles about Anthropic Company and tell me the highest scoring of them."
    final_answer = agent.run(user_input)
    print("Final Answer:", final_answer)

    user_input_2 = "Please help me with my search for the current weather in Arlington, Virginia."
    final_answer_2 = agent.run(user_input_2)
    print("Final Answer:", final_answer_2)
if __name__ == "__main__":
    main()
