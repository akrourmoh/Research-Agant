from tavily import TavilyClient
from graph.state import AgentState
from dotenv import load_dotenv
import os

load_dotenv()

def searcher_agent(state: AgentState) -> dict:
    client = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))
    results = []

    for sub_question in state["sub_questions"]:
        response = client.search(
            query=sub_question,
            max_results=3,
            search_depth="advanced"
        )

        for item in response["results"]:
            results.append(f"Source: {item['url']}\n{item['content']}")

    return {"search_results": results}



