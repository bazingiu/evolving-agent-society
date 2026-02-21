# 🤖 LangGraph Scaffold - AI Instructions

This document provides explicit guidelines for AI coding assistants (like Cursor, Copilot, or Claude) on how to understand, extend, and properly use the pieces of this LangGraph template framework.

**Every time you are instantiated in this repository, READ THIS FILE to understand the architectural rules.**

---

## 🏗️ Architecture Philosophy

This project uses a modular **Multi-Agent** architectural pattern with an Intelligent Supervisor (`Orchestrator`) and multiple independent Sub-Graphs (`Agents`). It strictly enforces **separation of concerns** between global routing and local agent execution.

### 1. State Management (Global vs Local)
- **`core/state.py` (`GlobalState`)**: The global router. It contains minimal routing info (`messages`, `task`, `active_agent`, `final_output`). **Do not add agent-specific fields here.**
- **`src/agents/<agent_name>/state.py` (`Private State`)**: Each agent defines its own isolated typed dict (e.g., `ExecutionAgentState`). An agent can track its own internal reasoning loops without polluting the `GlobalState`.

### 2. LLM Factory (Singleton)
- **Never instantiate LLMs directly** with `ChatGoogleGenerativeAI(...)` or `ChatOllama(...)`.
- **Always import** from the factory: 
  ```python
  from shared.llm import get_google_llm, get_ollama_llm
  llm = get_google_llm(temperature=0)
  ```
  *Why? Because it uses `@lru_cache` to ensure the same model instance is reused, preventing memory and connection overhead.*

### 3. Agent Sub-Graph Structure
Every agent logic belongs in its isolated folder under `src/agents/`. When modifying an agent, you should almost never need to touch files outside its folder. An agent directory usually looks like this:
- `config.py`: Instantiates `AgentConfig` (from `shared.base_agent_config.py`).
- `state.py`: Defines the agent's private typed dict.
- `nodes.py`: Contains the functional logic representation of nodes.
- `tools.py`: Any LangChain `@tool` functions used exclusively by this agent.
- `edges.py`: Logic for conditional routing between the agent's nodes.
- `graph.py`: Connects nodes and edges into a `StateGraph`, then `compile()` and export it.
- `prompts/system_prompt.md`: The dedicated prompt. Provide paths to this text instead of hardcoding prompts in python files where possible.

---

## � Initialization: Starting a New Project

When you (the AI) are starting a new project based on this scaffold, the **very first thing** you should do is prune what is not needed:
1. **Remove Unused Agents:** Delete the template agent folders (e.g., `src/agents/execution_agent` or `src/agents/research_agent`) if they are entirely irrelevant to the new project's specific requirements.
2. **Clean the Orchestrator:** Update `src/core/supervisor.py` and `src/main_graph.py` to remove the routing logic and imports for the agents you just deleted.
3. **Adapt the Global State:** If the new project needs a fundamentally different shared state, update `core/state.py`.
4. **Update README & Dependencies:** Prune anything that isn't needed by the new core logic.

Your goal isn't to force the new project into using `execution_agent`, but to use the *patterns* (Local vs Global state, LLM factory, independent sub-graphs) to build the right agents for the job.

---

## �🛠️ How to Add a New Agent

When you (the AI) are asked to create a new agent (e.g., `copywriting_agent`), follow this exact sequence:

### Step 1: Scaffold the Sub-Graph
1. Scaffold the agent folder: `src/agents/copywriting_agent/`.
2. Define the schema in `state.py` (e.g., `CopywritingAgentState`).
3. Create `config.py` leveraging the `shared.base_agent_config.AgentConfig`.
4. Create specific tools in `tools.py` (if any).
5. Code the functional behavior in `nodes.py` (importing `.state`, `.config`, `.tools`).
6. Build the sub-graph in `graph.py`:
   ```python
   from langgraph.graph import StateGraph, END
   from .state import CopywritingAgentState
   from .nodes import my_node
   
   def build_copywriting_agent_graph():
       builder = StateGraph(CopywritingAgentState)
       builder.add_node("main_node", my_node)
       builder.set_entry_point("main_node")
       builder.add_edge("main_node", END)
       return builder.compile()

   copywriting_agent_graph = build_copywriting_agent_graph()
   ```

### Step 2: Register in the Orchestrator
Once your sub-graph is compiled, integrate it into the global graph:
1. Expand the LLM routing capabilities in `src/core/supervisor.py`:
   - Update `RouteSchema` Literal adding `"copywriting_agent"`.
   - Update the `system_prompt` within `orchestrator_node` to explain exactly *when* the supervisor should route to `"copywriting_agent"`.
2. Connect it in `src/main_graph.py`:
   - Import it: `from agents.copywriting_agent.graph import copywriting_agent_graph`
   - Add it as a node: `builder.add_node("copywriting_agent", copywriting_agent_graph)`
   - Add transition in `route_agent` conditionals (implicitly works if it returns `active_agent`, just update the `RouteSchema` mapping dictionary).
   - Link its termination: `builder.add_edge("copywriting_agent", END)` (or map it back to `orchestrator` if recursive refinement is needed).

---

## 🧪 Testing Guidelines
- Use pytest (`make test`).
- Sub-Graphs can be tested in isolation inside `tests/unit/` using mock LLMs.
- The global orchestrator workflow is tested in `tests/integration/`.

## 📌 Checklist before writing code
- [ ] Check if you can use the LLM Factory instead of adding new dependencies.
- [ ] Check if the state variable you're adding belongs globally (`core/state.py`) or locally in the specific agent's `state.py`.
- [ ] Always ensure tools and variables are well typed with Python hints and `TypedDict` or `Pydantic`.
