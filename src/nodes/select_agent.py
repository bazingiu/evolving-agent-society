import random

from core.state import GlobalState


def select_agent(state: GlobalState):
    agents = state["agents"]
    selected = random.choice(agents)
    return {"current_agent_id": selected["id"]}
