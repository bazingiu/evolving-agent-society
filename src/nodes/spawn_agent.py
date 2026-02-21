from uuid import uuid4

from langchain_core.messages import HumanMessage

from core.state import Agent, GlobalState
from shared.llm import get_ollama_llm

llm = get_ollama_llm()


def spawn_agent(state: GlobalState):
    agents = list(state["agents"])
    fittest = max(agents, key=lambda a: a["fitness"])

    memory_text = "\n".join(state["collective_memory"])

    prompt = f"""Una società di agenti sta cercando di risolvere il seguente task: {state["task"]}
L'agente migliore finora ha questa personalità: {fittest["personality"]}

Memoria collettiva recente:
{memory_text}

Genera una breve descrizione della personalità per un nuovo agente "figlio". 
Il figlio deve ereditare i punti di forza del genitore (l'agente migliore) ma avere una specializzazione leggermente diversa suggerita dalle scoperte recenti. 
Restituisci SOLO la descrizione della personalità descritta in linguaggio naturale."""

    response = llm.invoke([HumanMessage(content=prompt)])
    
    child: Agent = {
        "id": str(uuid4())[:8],
        "name": f"Agent_{len(agents)+1}_Gen{fittest['generation']+1}",
        "personality": response.content.strip(),
        "generation": fittest["generation"] + 1,
        "fitness": 0.0
    }

    agents.append(child)
    return {"agents": agents}
