from dotenv import load_dotenv
from langgraph.checkpoint.base import BaseCheckpointSaver
from langgraph.graph import END, START, StateGraph

from core.state import Agent, GlobalState
from memory.checkpointer import get_checkpointer
from nodes import (
    end_node,
    evaluate,
    explore,
    select_agent,
    spawn_agent,
    update_culture,
)

load_dotenv()


def route_after_evaluate(state: GlobalState):
    cycle = state["cycle"]
    max_cycles = state["max_cycles"]

    if cycle >= max_cycles:
        return "end_node"
    if cycle % 3 == 0:
        return "spawn_agent"
    return "select_agent"


def build_main_graph(checkpointer: BaseCheckpointSaver | None = None):
    builder = StateGraph(GlobalState)

    builder.add_node("select_agent", select_agent)
    builder.add_node("explore", explore)
    builder.add_node("update_culture", update_culture)
    builder.add_node("evaluate", evaluate)
    builder.add_node("spawn_agent", spawn_agent)
    builder.add_node("end_node", end_node)

    builder.add_edge(START, "select_agent")
    builder.add_edge("select_agent", "explore")
    builder.add_edge("explore", "update_culture")
    builder.add_edge("update_culture", "evaluate")

    builder.add_conditional_edges(
        "evaluate",
        route_after_evaluate,
        {
            "end_node": "end_node",
            "spawn_agent": "spawn_agent",
            "select_agent": "select_agent",
        },
    )

    builder.add_edge("spawn_agent", "select_agent")
    builder.add_edge("end_node", END)

    return builder.compile(checkpointer=checkpointer)

# Global instance for print_graph
main_graph = build_main_graph(get_checkpointer())

if __name__ == "__main__":
    _checkpointer = get_checkpointer()
    _graph = build_main_graph(_checkpointer)

    _initial_agents: list[Agent] = [
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

    _initial_state: GlobalState = {
        "task": user_task,
        "agents": _initial_agents,
        "collective_memory": [],
        "current_discovery": "",
        "current_agent_id": "",
        "cycle": 0,
        "max_cycles": 9,
    }

    config = {"configurable": {"thread_id": "society_sim_run_1"}}

    print(f"🌍 Iniziando la simulazione per il task: {_initial_state['task']}")
    print(f"Limite cicli: {_initial_state['max_cycles']}\n")

    for event in _graph.stream(_initial_state, config=config):
        for node_name, state_update in event.items():
            if node_name == "explore":
                print(f"[{node_name}] Nuova scoperta registrata:")
                print(f"--> {state_update.get('current_discovery')}\n")
            elif node_name == "evaluate":
                print(f"[{node_name}] Ciclo completato: {state_update.get('cycle')}\n")
            elif node_name == "spawn_agent":
                agent = state_update.get("agents", [])[-1]
                print(
                    f"[{node_name}] ✨ Nuovo agente generato! {agent['name']} (Gen {agent['generation']})"
                )
                print(f"   Personalità: {agent['personality']}\n")
