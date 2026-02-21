from langchain_core.messages import HumanMessage

from core.state import GlobalState
from shared.llm import get_ollama_llm

llm = get_ollama_llm()


def explore(state: GlobalState):
    agents = state["agents"]
    current_agent = next(a for a in agents if a["id"] == state["current_agent_id"])

    memory_text = (
        "\n".join(state["collective_memory"])
        if state.get("collective_memory")
        else "Nessuna scoperta precedente."
    )

    prompt = f"""Sei un agente con la seguente personalità: {current_agent["personality"]}
Il problema che la società deve risolvere è: {state["task"]}

Ecco la memoria collettiva e le scoperte fatte finora:
{memory_text}

Produci esattamente UNA singola nuova scoperta o euristica per aiutare a risolvere il problema, che non sia già presente nella memoria collettiva. Sii conciso."""

    response = llm.invoke([HumanMessage(content=prompt)])
    discovery = response.content.strip()
    return {"current_discovery": discovery}
