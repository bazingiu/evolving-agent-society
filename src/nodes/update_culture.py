from langchain_core.messages import HumanMessage

from core.state import GlobalState
from shared.llm import get_ollama_llm

llm = get_ollama_llm()


def update_culture(state: GlobalState):
    new_memory = list(state.get("collective_memory", []))
    new_memory.append(state["current_discovery"])

    if len(new_memory) > 10:
        memory_text = "\n".join(new_memory)
        prompt = f"""Ecco la memoria collettiva di una società di agenti:
{memory_text}

Sintetizza queste scoperte in un massimo di 7 euristiche chiave, compatte e utili.
Restituisci SOLO la nuova lista di euristiche, una per riga, senza altra formattazione."""
        
        response = llm.invoke([HumanMessage(content=prompt)])
        lines = response.content.strip().split('\n')
        # Cleanup potential markers
        new_memory = [line.lstrip('- *').strip() for line in lines if line.strip()]

    return {"collective_memory": new_memory}
