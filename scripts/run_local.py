import sys
from pathlib import Path

from core.state import GlobalState
from dotenv import load_dotenv
from langchain_core.messages import HumanMessage
from main_graph import main_graph

load_dotenv()

# Aggiunge src al path
sys.path.append(str(Path(__file__).parent.parent / "src"))


def main():
    print("Inizializzando il grafo per testare LangSmith...")

    # Crea uno stato iniziale semplice
    _initial_agents = [
        {
            "id": "a1",
            "name": "Agente 1",
            "personality": "curioso e creativo, esplora idee non convenzionali",
            "generation": 0,
            "fitness": 0.0,
        },
        {
            "id": "a2",
            "name": "Agente 2",
            "personality": "critico e analitico, valuta i punti deboli delle soluzioni",
            "generation": 0,
            "fitness": 0.0,
        },
        {
            "id": "a3",
            "name": "Agente 3",
            "personality": "pragmatico orientato all'azione, cerca soluzioni applicabili subito",
            "generation": 0,
            "fitness": 0.0,
        },
    ]

    user_task = input("\nInserisci il task per la simulazione: ")
    if not user_task.strip():
        user_task = "Come può un sistema di AI migliorare progressivamente la sua capacità di rispondere a domande complesse?"
        print(f"Task vuoto. Uso il default: {user_task}")

    initial_state = {
        "task": user_task,
        "agents": _initial_agents,
        "collective_memory": [],
        "current_discovery": "",
        "current_agent_id": "",
        "cycle": 0,
        "max_cycles": 9,
    }

    print("Esecuzione nodo iniziale...")

    config = {"configurable": {"thread_id": "test_langsmith_1"}}

    for chunk in main_graph.stream(initial_state, config=config):
        for node_name, state_update in chunk.items():
            print(f"--- Finito nodo: {node_name} ---")

    # Stampa i messaggi finali
    # final_state = main_graph.get_state(config)
    print("\nEsecuzione terminata. Verifica la dashboard di LangSmith!")


if __name__ == "__main__":
    main()
