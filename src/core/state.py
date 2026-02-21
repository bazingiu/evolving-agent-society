from typing_extensions import TypedDict


class Agent(TypedDict):
    id: str
    name: str
    personality: str
    generation: int
    fitness: float


class GlobalState(TypedDict):
    """Global state for the evolutionary agent society."""

    task: str
    agents: list[Agent]
    collective_memory: list[str]
    current_discovery: str
    current_agent_id: str
    cycle: int
    max_cycles: int
