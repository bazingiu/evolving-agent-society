# Specifiche: Società di Agenti Evolutiva su LangGraph

---

## Contesto e Obiettivo

Implementare una società di agenti evolutiva usando il template preconfigurato di LangGraph. Il sistema deve simulare una cultura collettiva che si accumula nel tempo, agenti che generano nuovi agenti, e un feedback ambientale che valuta la qualità delle scoperte. Si parte da zero agenti preconfigurati — la conoscenza emerge dall'esperienza.

---

## Stato del Grafo

Definisci uno stato `TypedDict` con questi campi:

| Campo | Tipo | Descrizione |
|---|---|---|
| `task` | `str` | Il problema che la società deve risolvere |
| `agents` | `list[dict]` | Lista agenti con `id`, `name`, `personality`, `generation`, `fitness` |
| `collective_memory` | `list[str]` | Scoperte e euristiche accumulate dalla società |
| `current_discovery` | `str` | Ultima scoperta prodotta |
| `current_agent_id` | `str` | ID dell'agente che sta lavorando |
| `cycle` | `int` | Contatore dei cicli completati |
| `max_cycles` | `int` | Limite massimo di cicli |

---

## Agenti Iniziali

Al momento dell'inizializzazione, crea **3 agenti di partenza** con personalità diverse descritte in linguaggio naturale:

- **Agente 1** — curioso e creativo, esplora idee non convenzionali
- **Agente 2** — critico e analitico, valuta i punti deboli delle soluzioni
- **Agente 3** — pragmatico orientato all'azione, cerca soluzioni applicabili subito

Tutti partono con `generation=0` e `fitness=0.0`.

---

## Nodi del Grafo

### Nodo 1 — `select_agent`

Seleziona casualmente un agente dalla lista. Salva il suo id in `current_agent_id`. Non chiama nessun LLM, è solo logica di selezione.

---

### Nodo 2 — `explore`

Costruisce un prompt che contiene:
- La personalità dell'agente selezionato
- Il task corrente
- Tutta la memoria collettiva accumulata

Chiede al modello di produrre **una sola scoperta o euristica nuova**, che non sia già presente nella memoria collettiva. L'output viene salvato in `current_discovery`.

---

### Nodo 3 — `update_culture`

- Aggiunge `current_discovery` alla `collective_memory`
- Se la memoria supera **10 elementi**, chiama il modello e chiedigli di sintetizzare tutta la memoria in **massimo 7 euristiche chiave**, compatte e utili
- Sostituisce la memoria con la versione sintetizzata

---

### Nodo 4 — `evaluate`

- Chiama il modello passandogli il task e la scoperta appena prodotta
- Chiede un **punteggio da 0.0 a 1.0** con una breve motivazione
- Aggiorna il campo `fitness` dell'agente corrente con questo punteggio
- Incrementa `cycle` di 1
- Se il parsing del punteggio fallisce → assegna `0.5` come default

---

### Nodo 5 — `spawn_agent`

> Attivato **solo ogni 3 cicli**

- Prende l'agente con il **fitness più alto**
- Chiama il modello chiedendogli di generare un nuovo agente figlio con:
  - Una personalità che eredita i punti di forza del genitore
  - Una specializzazione leggermente diversa, suggerita dalle ultime scoperte nella memoria collettiva
- Il nuovo agente ha `generation = genitore.generation + 1` e `fitness = 0.0`
- Aggiunge il nuovo agente alla lista `agents`

---

### Nodo Finale — `end`

Chiama il modello passandogli:
- Tutta la memoria collettiva
- La lista degli agenti con i loro fitness
- Il task originale

Produce un **report finale** con:
1. Le 5 scoperte più importanti emerse
2. I ruoli che si sono specializzati nella società
3. Una valutazione di quanto la società ha progredito

---

## Logica di Routing

Dopo il nodo `evaluate`, controlla:

```
se cycle >= max_cycles     →  vai a END
se cycle % 3 == 0          →  vai a spawn_agent → poi torna a select_agent
altrimenti                 →  torna a select_agent
```

---

## Configurazione del Grafo

- **Entry point**: `select_agent`
- Usa `StateGraph` con lo stato definito sopra
- Compila il grafo con `MemorySaver` come checkpointer per la persistenza
- `max_cycles` di default: **9** (spawn_agent viene chiamato 3 volte → 3 generazioni)

---

## Esecuzione

Alla fine del file, aggiungi un blocco di esecuzione con un task di esempio:

> *"Come può un sistema di AI migliorare progressivamente la sua capacità di rispondere a domande complesse?"*

Con `max_cycles=9`. Il programma deve:
- Stampare ogni scoperta man mano che viene prodotta
- Stampare il report finale al termine

---

## Vincoli Tecnici

- Usa solo le librerie già presenti nel template LangGraph preconfigurato
- Il modello da usare è quello già configurato nel template — non hardcodare nessuna API key
- Ogni chiamata al modello deve avere un prompt chiaro e restituire testo plain, nessun JSON parsing complesso
- Se il parsing di un punteggio numerico fallisce, assegna `0.5` come default
- Genera del codice che rispetti i principi solid
sia ben organizzaro dry e segua le good practise
- Voglio essere io a ogni step ad autorizzalo ad andare avanti