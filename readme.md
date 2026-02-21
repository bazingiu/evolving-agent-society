# 🤖 My LangGraph Project

Progetto multi-agente basato su [LangGraph](https://github.com/langchain-ai/langgraph).  
Supporta **Google Gemini** e **Ollama** come provider LLM, con architettura DRY basata su una graph factory parametrizzata.

---

## 📁 Struttura del Progetto

```
my-langgraph-project/
│
├── src/
│   ├── main_graph.py                  # Entry point: istanzia il grafo Supervisore
│   ├── core/                          # Logica di orchestrazione globale
│   │   └── state.py                   # GlobalState: lo stato condiviso tra tutti gli agenti
│   │
│   ├── agents/                        # I Sub-Grafi (Gli Agenti)
│   │   ├── execution_agent/           # Dipartimento / Agente Esecutore
│   │   │   ├── config.py              # Definizione config e istanziazione LLM base
│   │   │   ├── edges.py               # Logica di routing condizionale interna
│   │   │   ├── graph.py               # Costruzione del sub-grafo per Execution Agent
│   │   │   ├── nodes.py               # Nodi specifici di elaborazione
│   │   │   ├── state.py               # Private State isolato dell'agente (ExecutionAgentState)
│   │   │   ├── tools.py               # Tool ad uso esclusivo dell'agente esecutore
│   │   │   └── prompts/
│   │   │       └── system_prompt.md   # Prompt isolati per l'agente
│   │   │
│   │   └── research_agent/            # Dipartimento / Agente Ricercatore
│   │       └── ...                    # Stessa struttura isolata di execution_agent
│   │
│   ├── shared/                        # Componenti riutilizzabili cross-agent
│   │   ├── base_agent_config.py       # Definizione della data class `AgentConfig`
│   │   └── llm.py                     # LLM factory unificata (Google + Ollama)
│   │
│   └── memory/                        # Persistenza dello stato tra sessioni
│       ├── checkpointer.py            # Checkpointer (MemorySaver / PostgresSaver)
│       └── store.py                   # Long-term memory store
│
├── tests/
│   ├── conftest.py                    # Fixture pytest condivise (es. base_state)
│   ├── unit/                          # Test dei singoli nodi in isolamento
│   └── integration/                   # Test dell'intero grafo end-to-end
│
├── scripts/
│   └── run_local.py                   # Esecuzione manuale per test rapidi
│
├── .docker/
│   ├── Dockerfile                     # Immagine Docker del progetto
│   └── docker-compose.yml             # Orchestrazione: agent
│
├── .env                               # Variabili d'ambiente reali (non in git)
├── .env.example                       # Template delle variabili (in git)
├── langgraph.json                     # Config per LangGraph CLI e LangSmith
├── pyproject.toml                     # Dipendenze e metadata del progetto
└── README.md
```

---

## 🧠 Concetti Chiave

### GlobalState vs Private State (Local State)
L'architettura separa lo stato in due livelli per massimizzare la pulizia e l'isolamento:

1. **`core/state.py` (GlobalState):** È il "carrello" globale gestito dall'Orchestratore (Supervisor). Contiene solo le info necessarie per passare il lavoro tra un agente e l'altro (es. la lista dei messaggi e quale agente deve elaborare il task).
2. **`agents/<nome_agente>/state.py` (Private State):** Ogni sub-grafo/agente ha il suo stato locale isolato. Questo permette a un agente di "ricordarsi" calcoli intermedi interni senza sporcare il GlobalState.

---

### LLM Factory (`shared/llm.py`)
Unica fonte per l'istanziazione dei modelli LLM. Tutti i nodi chiamano
`get_google_llm()` o `get_ollama_llm()` — nessuno istanzia modelli inline.

Il decoratore `@lru_cache` garantisce che lo stesso modello venga creato
**una volta sola** in memoria, indipendentemente da quante volte viene chiamato.

```python
# In qualsiasi nodo:
from agents.shared.llm import get_google_llm

llm = get_google_llm()  # istanza cached, zero boilerplate
```

---

### Struttura Ad Agenti (Sub-Graphs)
A differenza di framework monolitici, qui **ogni Agente è un Sub-Grafo indipendente**.

* **Isolamento delle Feature:** Se devi modificare l'Execution Agent per usare nuovi tool o avere una diversa logica di routing, lavori esclusivamente dentro `src/agents/execution_agent/`. Nessun altro agente ne sarà influenzato.
* **Costruzione del Grafo:** Ogni cartella `agent_x` contiene un file `graph.py` che costruisce e compila logicamente e in modo isolato la propria macchina a stati (Sub-Grafo).

### L'Orchestratore (Supervisor)
In `src/main_graph.py` (o all'interno di `core/`) risiede il grafo principale. Il suo scopo NON è processare i dati operativamente, ma fare routing logico e decidere a quale Sub-Grafo/Agente passare il controllo leggendo il `GlobalState`.

```
Orchestrator ──┐
               ├──▶ (Sub-Graph) Agent A ──▶ Fine Task
               └──▶ (Sub-Graph) Agent B ──▶ Fine Task
```

## 🚀 Avvio in Locale

### Con Docker (raccomandato)

```bash
# Copia e compila le variabili d'ambiente
cp .env.example .env
# → Apri .env e inserisci GOOGLE_API_KEY e le altre chiavi

# Assicurati di avere Ollama avviato localmente dal tuo host PC!

# Avvia il container (agent)
make build    # esegue il build e lancia docker compose up
# oppure
make up       # se l'immagine esiste già, lancia soltanto docker compose up
```

### Visualizzazione del Grafo

Puoi generare un'immagine PNG dell'architettura del tuo grafo eseguendo il seguente script:

```bash
make graph
```

L'immagine verrà salvata nella cartella `output/` come `graph_main.png`.

### Comando Rapidi tramite `Makefile`

Per comodità, il progetto include un `Makefile` con comandi rapidi. **Se usi Windows**, puoi installare Make tramite `winget install GnuWin32.Make` per usufruire di questi comandi:

| Comando | Descrizione |
|---|---|
| `make up` | Avvia i container normalmente (`docker compose up`) |
| `make build` | Fa la build e avvia i container (`docker compose up --build`) |
| `make down` | Spegne i container |
| `make test` | Lancia pytest all'interno del container Docker |
| `make graph` | Genera l'immagine dell'architettura in `output/graph_main.png` |

---

### Senza Docker

```bash
# Installa le dipendenze
pip install -e ".[dev]"

# Carica le variabili e avvia
python scripts/run_local.py
```

---

## 🧪 Test

```bash
# Tutti i test (usando make)
make test
```

I test unitari mockano il LLM per testare ogni nodo in isolamento.
I test di integrazione usano modelli reali e verificano il comportamento
dell'intero grafo end-to-end.

---

## 🔧 Variabili d'Ambiente

| Variabile | Obbligatoria | Descrizione |
|-----------|-------------|-------------|
| `GOOGLE_API_KEY` | ✅ | API key di Google AI Studio |
| `OLLAMA_BASE_URL` | ✅ | URL di Ollama (default: `http://host.docker.internal:11434`) |
| `LANGCHAIN_TRACING_V2` | ⚪ | Abilita il tracing su LangSmith (`true`/`false`) |
| `LANGCHAIN_API_KEY` | ⚪ | API key di LangSmith |
| `LANGCHAIN_PROJECT` | ⚪ | Nome del progetto su LangSmith |

---

## 🕷️ Configurazione LangSmith (Tracing)

LangSmith ti permette di tracciare, profilare e debuggare le esecuzioni dei tuoi agenti LangGraph in tempo reale. Questo scaffold è già pre-configurato per supportarlo in ogni ambiente.

### Come collegare LangSmith:

1. **Crea un account e ottieni l'API Key:**
   - Vai su [LangSmith](https://smith.langchain.com/) e registrati / accedi.
   - Vai in **Settings -> API Keys** e genera una nuova API Key.
   - (Opzionale) Crea un nuovo progetto dal menu laterale se non vuoi usare `default` e segnati il nome.

2. **Configura il file `.env`:**
   - Apri il file `.env` alla radice del tuo progetto (copiandolo da `.env.example` se necessario).
   - Inserisci le tue credenziali e assicurati che il flag `TRACING_V2` sia attivo:
     ```env
     LANGCHAIN_TRACING_V2=true
     LANGCHAIN_API_KEY=lsv2_pt_tua_api_key_qui_...
     LANGCHAIN_PROJECT=my-langgraph-project
     ```

3. **Inizia a tracciare:**
   - **Tramite Docker**: Quando avvii i log con `make up` (`docker compose up`), il file `docker-compose.yml` importerà e applicherà automaticamente le variabili LangSmith ai container.
   - **Script Locali**: I file entry point (`src/main_graph.py`, `src/print_graph.py`) utilizzano `load_dotenv()` ed espongono internamente all'interprete di Python l'ambiente di tracciamento LangSmith.
   - **LangGraph Studio**: Il settings in `langgraph.json` è già preimpostato in lettura (`"env": ".env"`). 

A questo punto, le prossime esecuzioni dei grafi o chiamate agli agent registreranno automaticamente tutti i layer e tool chiamati nella dashboard web del tuo LangSmith.

---

## 📦 Dipendenze Principali

| Pacchetto | Scopo |
|-----------|-------|
| `langgraph` | Framework per la costruzione dei grafi agentici |
| `langchain-google-genai` | Integrazione con Google Gemini |
| `langchain-ollama` | Integrazione con Ollama (modelli locali) |
| `langchain-core` | Astrazioni base di LangChain (tools, prompts, ecc.) |
| `pydantic` | Validazione e serializzazione dei dati |
| `python-dotenv` | Caricamento variabili da `.env` |

---

## 🗺️ Prossimi Passi
- [ ] Implementare i nodi in `core/nodes/`
- [ ] Implementare la logica di routing in `core/edges/routing.py`
- [ ] Aggiungere i tool in `shared/tools/`
- [ ] Scrivere i primi unit test in `tests/unit/`