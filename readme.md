# 🧬 Evolutionary Agent Society (on LangGraph)

This project implements an **evolutionary agent society** based on [LangGraph](https://github.com/langchain-ai/langgraph).
The system simulates a collective culture that accumulates over time, agents that spawn new progeny agents, and an environmental feedback loop that evaluates the quality of discoveries. The simulation starts with 3 pre-configured agents, and knowledge emerges iteratively through experience.

It supports local LLMs such as **Ollama** (`llama3`) or via API through the LLM Factory in `shared`.

---

## 🎯 System Objective

The simulation revolves around solving a complex `task` by looping through cycles of exploration, cultural synthesis, and evaluation.

1. A random agent is selected from the society.
2. The agent leverages its *personality* and the *collective memory* to propose a **new discovery**.
3. The discovery is appended to the **collective memory** (which is periodically synthesized into more compact heuristics if it grows too large).
4. The discovery is evaluated and the agent is assigned a fitness score.
5. Every 3 cycles, the most "fit" agent (the best performer) spawns a **new child agent**, combining the winning traits of the parent with the needs highlighted by recent discoveries in the society.
6. Finally, a concluding report on the society's progress is emitted.

---

## 📁 Project Structure

```
my-langgraph-project/
│
├── src/
│   ├── main_graph.py                  # Entry point and StateGraph assembly
│   ├── core/
│   │   └── state.py                   # Global state and agent definitions
│   │
│   ├── nodes/                         # Isolated graph nodes
│   │   ├── select_agent.py            # Selects the active agent
│   │   ├── explore.py                 # Generates a new discovery
│   │   ├── update_culture.py          # Manages and synthesizes collective memory
│   │   ├── evaluate.py                # Calculates fitness for the discovery
│   │   ├── spawn_agent.py             # Spawns a new child agent
│   │   └── end_node.py                # Prints the final report
│   │
│   └── shared/                        
│       └── llm.py                     # Unified model provider (e.g., Ollama)
```

## 🚀 Local Setup

### Prerequisites: Ollama

The project is configured to use **Ollama** by default, pointing to your host machine's address (when running inside Docker).
You must have Ollama running in the background on your PC and the `llama3` model downloaded:

```bash
ollama serve
ollama pull llama3
```

### Starting (With Docker)

```bash
make build    # builds and runs the image
# or
make run script=scripts/run_local.py  # executes the simulation
```

### Graph Visualization

You can generate a PNG image of your graph's architecture by running the following script:

```bash
make graph
```

The image will be saved in the `output/` folder as `graph_main.png`.

---

## 🔧 Environment Variables

To run the framework smoothly (without hardcoding keys), copy `.env.example` to `.env`.

| Variable | Description |
|-----------|-------------|
| `OLLAMA_BASE_URL` | URL of your Ollama instance (default: `http://host.docker.internal:11434` for Docker usage) |
| `LANGCHAIN_TRACING_V2` | Enable LangSmith (`true`/`false`), optional. |

---

## 🛠️ Modifying the Simulation (Initial Task)
To change the starting question/problem for the society, open `scripts/run_local.py` or the `__main__` block in `src/main_graph.py` and edit the `task` string inside the `initial_state`.