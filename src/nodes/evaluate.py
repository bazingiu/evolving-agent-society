import re

from langchain_core.messages import HumanMessage

from core.state import GlobalState
from shared.llm import get_ollama_llm

llm = get_ollama_llm()


def evaluate(state: GlobalState):
    prompt = f"""Valuta la seguente scoperta proposta per questo task.
Task: {state["task"]}
Scoperta: {state["current_discovery"]}

Assegna un punteggio di fitness da 0.0 a 1.0 che rappresenti quanto questa scoperta è utile e originale.
Fornisci una breve motivazione, poi scrivi il punteggio nell'ultima riga nel formato: 'Score: [numero]'"""

    response = llm.invoke([HumanMessage(content=prompt)])
    content = response.content

    score = 0.5
    match = re.search(r'Score:\s*([0-9]*\.?[0-9]+)', content)
    if match:
        try:
            score = float(match.group(1))
        except ValueError:
            score = 0.5

    agents = list(state["agents"])
    for a in agents:
        if a["id"] == state["current_agent_id"]:
            a["fitness"] = score # spec: "Aggiorna il campo fitness dell'agente corrente con questo punteggio"
            break

    cycle = state.get("cycle", 0) + 1
    return {"agents": agents, "cycle": cycle}
