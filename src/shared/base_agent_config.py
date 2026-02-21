from dataclasses import dataclass, field

from langchain_core.tools import BaseTool


@dataclass
class AgentConfig:
    name: str
    system_prompt: str
    tools: list[BaseTool] = field(default_factory=list)
    llm_provider: str = "google"
    model: str = "gemini-1.5-pro"
    temperature: float = 0.0
