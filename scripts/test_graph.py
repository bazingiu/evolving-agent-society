import asyncio

from dotenv import load_dotenv
from langchain_core.messages import HumanMessage

from src.main_graph import main_graph

load_dotenv()


async def run_test():
    # 1. Test routing to execution_agent (natural language)
    print("\n\n=== Test 1: Routing to Execution Agent ===")
    state_a = {
        "messages": [HumanMessage(content="Hello, running a test")],
        "task": "Mi serve un test sull'intera applicazione",
        "active_agent": None,
        "final_output": None,
    }

    result_a = await main_graph.ainvoke(state_a)
    print(
        "Graph routed to:",
        result_a.get("active_agent", "Not set by nodes natively but trace will show"),
    )
    print("Execution Agent final message:", result_a["messages"][-1].content)

    # 2. Test routing to research_agent (RAG)
    print("\n\n=== Test 2: Routing to Research Agent (RAG) ===")
    state_rag = {
        "messages": [HumanMessage(content="Parlami della pizza")],
        "task": "Che documenti abbiamo sulla pizza margherita?",
        "active_agent": None,
        "final_output": None,
    }

    result_rag = await main_graph.ainvoke(state_rag)
    print("RAG Context retrieved:", result_rag.get("context"))
    print("RAG Final Output:\n", result_rag.get("final_output"))


if __name__ == "__main__":
    asyncio.run(run_test())
