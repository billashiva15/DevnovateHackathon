<div align="center">

# 🧠 DealMind AI
### Memory-Powered Sales Intelligence Agent

[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-009688?style=for-the-badge&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
[![Groq](https://img.shields.io/badge/Groq-qwen3--32b-F55036?style=for-the-badge&logo=groq&logoColor=white)](https://groq.com)
[![Hindsight](https://img.shields.io/badge/Hindsight-Memory_Layer-7C3AED?style=for-the-badge)](https://hindsight.dev)
[![Hackathon](https://img.shields.io/badge/Devnovate-Hackathon_2025-10B981?style=for-the-badge)](https://github.com/billashiva15/DevnovateHackathon)

> **DealMind AI** gives your sales team a memory — combining CRM deal data, persistent conversation memory via Hindsight, and blazing-fast LLM inference via Groq to suggest winning sales strategies in real time.

---

[📺 Video Demo](#-video-demo) • [🚀 Quick Start](#-quick-start) • [⚙️ API Setup](#️-api-key-setup) • [🧠 Architecture](#-architecture) • [📊 Dataset](#-dataset)

</div>

---

## 📸 Screenshots

### DealMind AI — Main Dashboard

![DealMind AI Dashboard](https://github.com/billashiva15/DevnovateHackathon/blob/main/Screenshot%202026-04-19%20042647.png)
> Client selector → Enter a message → Get AI-powered deal intelligence instantly

> *Three-panel layout: Client selector (left), Interaction + AI suggestion (center), Client brief + Memory (right)*

---

### 🧠 Hindsight Memory — Persistent Client Memory
> Hindsight stores and recalls every past interaction per client. The agent remembers what was said before — turning a stateless LLM into a relationship-aware assistant.

![Hindsight Memory Panel](https://github.com/billashiva15/DevnovateHackathon/blob/main/Screenshot%202026-04-19%20042743.png)
> *The "Client Memory" panel on the right grows over time as interactions are saved. On the next conversation with the same client, past context is automatically recalled.*

**How Hindsight memory works in DealMind:**

```
First interaction:   [No memory] → AI responds → Memory saved ✅
Second interaction:  [Memory loaded] → AI responds with full context ✅
Third interaction:   [Growing memory] → AI knows objections, preferences, history ✅
```

---



### work flow of Hindsight

![WorkFlow of Handsight].(https://github.com/billashiva15/DevnovateHackathon/blob/main/Screenshot%202026-04-19%20060157.png)

### 🔑 Groq + Hindsight API Keys — `.env` Setup

![API Keys Setup](docs/screenshots/api_keys_env.png)

> **Never hardcode API keys.** DealMind uses a `.env` file to keep credentials secure.

---

## ⚙️ API Key Setup

### Step 1 — Get your API keys

| Service | Where to get it | Purpose |
|---|---|---|
| **Groq** | [console.groq.com](https://console.groq.com) | LLM inference (qwen3-32b) |
| **Hindsight** | [app.hindsight.dev](https://app.hindsight.dev) | Persistent memory layer |

### Step 2 — Create your `.env` file

In the root of the project, create a file named `.env`:

```bash
# .env — DealMind AI Configuration

# ─── Groq LLM ─────────────────────────────────────────────
GROQ_API_KEY=gsk_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

# ─── Hindsight Memory ─────────────────────────────────────
HINDSIGHT_API_KEY=hs_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

# ─── App Config ───────────────────────────────────────────
APP_HOST=0.0.0.0
APP_PORT=8000
DEBUG=False
```

> ⚠️ The `.gitignore` already excludes `.env` — your keys will never be committed to GitHub.

### Step 3 — Load keys in your backend

```python
# backend/config.py
from dotenv import load_dotenv
import os

load_dotenv()

GROQ_API_KEY    = os.getenv("GROQ_API_KEY")
HINDSIGHT_API_KEY = os.getenv("HINDSIGHT_API_KEY")
```

---

## 🤖 LLM — Groq with `qwen3-32b`

DealMind uses **Groq's ultra-fast inference** with the `qwen3-32b` model for generating context-aware sales responses.

### Why `qwen3-32b`?

| Feature | Detail |
|---|---|
| **Model** | `qwen3-32b` |
| **Parameters** | 32 Billion |
| **Speed** | ~800 tokens/sec on Groq hardware |
| **Strength** | Strong reasoning, instruction following, multilingual |
| **Use case** | Sales strategy generation, objection handling |

### Implementation

```python
# backend/llm_engine.py

from groq import Groq
import os

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def generate_sales_reply(
    client_message: str,
    deal_context: dict,
    memory_context: str = ""
) -> str:
    """
    Generate a strategic sales reply using Groq qwen3-32b.
    
    Args:
        client_message  : The incoming message from the client
        deal_context    : Deal stage, value, product, objection type
        memory_context  : Past interactions recalled from Hindsight
    
    Returns:
        A concise, strategic sales reply string
    """

    system_prompt = f"""You are DealMind AI, an expert B2B sales intelligence assistant.

Deal Context:
- Account       : {deal_context.get('account_name')}
- Deal Stage    : {deal_context.get('stage')}
- Deal Value    : ${deal_context.get('value')}
- Product       : {deal_context.get('product')}
- Sales Agent   : {deal_context.get('owner')}
- Objection     : {deal_context.get('objection_type', 'general')}
- Strategy      : {deal_context.get('suggested_strategy')}

Past Interactions (Memory):
{memory_context if memory_context else 'No previous interactions found.'}

Rules:
- Be consultative, concise, and move toward the next action
- Keep reply under 3 sentences
- No markdown formatting, labels, or headers
- Match the deal stage tone (won = onboarding, proposal = persuade, etc.)
"""

    response = client.chat.completions.create(
        model="qwen3-32b",           # ← Groq qwen3-32b model
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user",   "content": client_message}
        ],
        temperature=0.7,
        max_tokens=200,
        stream=False
    )

    return response.choices[0].message.content.strip()
```

### Example response

```python
# Input
client_message = "We're interested but need to discuss pricing."
deal_context = {
    "account_name": "Acme Corporation",
    "stage": "Proposal",
    "value": 4980,
    "product": "GTXPro",
    "objection_type": "pricing",
    "suggested_strategy": "Be consultative, highlight ROI"
}

# Output from qwen3-32b
reply = generate_sales_reply(client_message, deal_context)
# → "Great to hear your interest in GTXPro! Given the ROI our 
#    clients typically see within 60 days, let's schedule a quick 
#    call to walk through the pricing tiers. Does Thursday work?"
```

---

## 🧠 Architecture

```
┌─────────────────────────────────────────────────────────┐
│                      DealMind AI                         │
├──────────────┬──────────────────────┬───────────────────┤
│  Frontend    │      Backend         │   Data Layer       │
│  (HTML/JS)   │     (FastAPI)        │   (CSV + Memory)   │
│              │                      │                    │
│  Client      │  ┌─────────────┐    │  deals_master.csv  │
│  Selector    │  │ Objection   │    │  accounts.csv      │
│              │  │ Detection   │    │  sales_pipeline    │
│  Message     │  └──────┬──────┘    │                    │
│  Input       │         │           │  ┌──────────────┐  │
│              │  ┌──────▼──────┐    │  │  Hindsight   │  │
│  AI          │  │  Deal Intel │◄───┤  │  Memory API  │  │
│  Suggestion  │  │  Engine     │    │  │              │  │
│              │  └──────┬──────┘    │  │  Per-client  │  │
│  Deal        │         │           │  │  memory store│  │
│  Intelligence│  ┌──────▼──────┐    │  └──────────────┘  │
│  Output      │  │  Groq LLM   │    │                    │
│              │  │  qwen3-32b  │    │                    │
│  Client      │  └──────┬──────┘    │                    │
│  Memory      │         │           │                    │
│  Panel       │  ┌──────▼──────┐    │                    │
│              │  │  Response   │    │                    │
│              │  │  + Save Mem │    │                    │
│              │  └─────────────┘    │                    │
└──────────────┴──────────────────────┴───────────────────┘
```

### CascadeFlow Pipeline

```
User Message
    │
    ▼
Objection Detection  ──►  [pricing / trust / general / timeline]
    │
    ▼
CRM Data Lookup  ──►  account, stage, value, product, owner
    │
    ▼
Hindsight Memory Recall  ──►  past interactions for this client
    │
    ▼
Strategy Engine  ──►  [be consultative / push urgency / onboard]
    │
    ▼
Groq qwen3-32b  ──►  generates reply (< 200 tokens, < 500ms)
    │
    ▼
Response Delivered  +  Memory Saved to Hindsight
```

---

## 📊 Dataset

**Source:** [Kaggle — B2B Sales CRM Dataset](https://www.kaggle.com)

| File | Records | Description |
|---|---|---|
| `accounts.csv` | 500 companies | Firmographics: sector, revenue, employees, location |
| `sales_pipeline.csv` | 8,800 deals | Stage, value, product, close date, agent |
| `products.csv` | 7 products | GTXPro, MG Special, GTX Plus, etc. |
| `sales_teams.csv` | 35 agents | Manager, region, team performance |
| `data_dictionary.csv` | — | Field definitions for all tables |

**Processed:** `data/processed/deals_master.csv` — joined, cleaned master table used by the intelligence engine.

---

## 🚀 Quick Start

### Prerequisites

```bash
Python 3.10+
pip
```

### Installation

```bash
# 1. Clone the repo
git clone https://github.com/billashiva15/DevnovateHackathon.git
cd DevnovateHackathon

# 2. Install dependencies
pip install -r requirements.txt

# 3. Set up your API keys
cp .env.example .env
# Edit .env and add your GROQ_API_KEY and HINDSIGHT_API_KEY

# 4. Run the backend
cd backend
uvicorn main:app --reload --host 0.0.0.0 --port 8000

# 5. Open the frontend
# Open frontend/index.html in your browser
# Or run a simple server:
cd frontend && python -m http.server 3000
```

### API Endpoints

```
POST /api/suggest          →  Get AI reply for a client message
GET  /api/deal/{account}   →  Fetch deal intelligence for an account
GET  /api/memory/{account} →  Get Hindsight memory for a client
POST /api/memory/save      →  Save an interaction to memory
```

---

## 📦 Project Structure

```
DevnovateHackathon/
├── backend/
│   ├── main.py              # FastAPI app entry point
│   ├── config.py            # Environment variable loader
│   ├── llm_engine.py        # Groq qwen3-32b integration
│   ├── memory_manager.py    # Hindsight memory read/write
│   ├── deal_intelligence.py # Objection detection + strategy engine
│   └── data_loader.py       # CRM CSV processing
├── data/
│   ├── raw/                 # Original Kaggle CSVs
│   └── processed/
│       └── deals_master.csv # Cleaned + joined master table
├── frontend/
│   ├── index.html           # Main dashboard UI
│   ├── app.js               # Frontend logic
│   └── style.css            # Dark theme styling
├── tests/
│   └── test_api.py          # API endpoint tests
├── docs/
│   └── screenshots/         # README images
├── .env.example             # Template for environment variables
├── .gitignore               # Excludes .env, __pycache__, etc.
├── requirements.txt         # Python dependencies
└── README.md
```

---

## 📋 Requirements

```txt
fastapi==0.110.0
uvicorn==0.27.0
groq==0.5.0
hindsight-sdk==1.0.0
pandas==2.2.0
python-dotenv==1.0.0
pydantic==2.6.0
httpx==0.27.0
```

---

## 🎯 Key Features

| Feature | Description |
|---|---|
| 🧠 **Persistent Memory** | Hindsight stores past interactions per client — agent remembers history across sessions |
| ⚡ **Fast Inference** | Groq `qwen3-32b` delivers sub-500ms response generation |
| 📊 **CRM-Grounded** | All suggestions anchored to real deal data — no generic LLM guesses |
| 🎯 **Objection Detection** | Automatically classifies client messages: pricing, trust, urgency, general |
| 🗺️ **Stage-Aware Strategy** | Adapts tone and strategy based on deal stage (Won / Proposal / Negotiation) |
| 🚨 **Risk Flags** | Surfaces deal risk indicators from CRM patterns |

---

## 🔮 Future Scope

- [ ] Deal win probability scoring
- [ ] Risk prediction dashboard
- [ ] Email draft generation
- [ ] Slack / CRM integration (Salesforce, HubSpot)
- [ ] Multi-agent team coordination
- [ ] Analytics dashboard for sales managers

---

## 🏆 Hackathon

Built for the **Devnovate Hackathon 2025** using:
- **CascadeFlow** — agentic pipeline orchestration
- **Hindsight** — persistent memory layer
- **Groq** — high-speed LLM inference

---

## 👨‍💻 Author

**Billa Shiva**
- GitHub: [@billashiva15](https://github.com/billashiva15)

---

<div align="center">

Built with ❤️ using **FastAPI** + **Groq** + **Hindsight**

⭐ Star this repo if you found it helpful!

</div>
