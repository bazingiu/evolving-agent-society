from langchain_core.messages import HumanMessage

from core.state import GlobalState
from shared.llm import get_ollama_llm

llm = get_ollama_llm()


def end_node(state: GlobalState):
    memory_text = "\n".join(state["collective_memory"])
    agents_text = "\n".join(
        [
            f"- {a['name']} (Gen {a['generation']}, Fitness {a['fitness']}): {a['personality']}"
            for a in state["agents"]
        ]
    )

    prompt = f"""La società di agenti ha terminato la simulazione per il task: {state["task"]}

Memoria Collettiva Finale:
{memory_text}

Agenti nella società al termine:
{agents_text}

Produci un report finale ben formattato in markdown con:
1. Le 5 scoperte più importanti emerse
2. I ruoli che si sono specializzati nella società
3. Una valutazione di quanto la società ha progredito"""

    response = llm.invoke([HumanMessage(content=prompt)])
    print("\n" + "=" * 50)
    print("REPORT FINALE DELLA SOCIETÀ")
    print("=" * 50)
    print(response.content)
    print("=" * 50 + "\n")
    return {}
