# Research Agent 🔍

An autonomous multi-agent AI system that researches any topic by searching the live web, writing a structured answer, and self-correcting until the quality is satisfactory.

---

## How it works

You submit a question. The system does everything else automatically:

```
User Question
      ↓
[Planner Agent]   → breaks the question into 3 focused sub-questions
      ↓
[Searcher Agent]  → searches the live web for each sub-question (up to 9 sources)
      ↓
[Writer Agent]    → synthesizes a structured, sourced answer
      ↓
[Critic Agent]    → reviews the answer strictly on 3 criteria
      ↓
   PASS? ──────────────────────→ Final answer delivered
      │
     FAIL
      │
      └──→ feedback sent back to Writer (max 3 revisions)
```

---

## Tech Stack

| Layer | Technology |
|---|---|
| LLM | Gemini (Google AI) |
| Orchestration | LangGraph |
| Agent Framework | LangChain |
| Web Search | Tavily API |
| Observability | LangSmith |
| Backend API | FastAPI |
| Frontend | HTML, CSS, JavaScript |
| Containerization | Docker |

---

## Project Structure

```
research-agent/
├── agents/
│   ├── planner.py       # breaks question into sub-questions
│   ├── searcher.py      # searches the web via Tavily
│   ├── writer.py        # writes structured answer
│   └── critic.py        # reviews and loops back if needed
├── graph/
│   ├── state.py         # shared state between all agents
│   └── workflow.py      # LangGraph graph definition
├── api/
│   └── main.py          # FastAPI REST API
├── frontend/
│   ├── index.html       # web interface
│   ├── style.css        # styling
│   └── app.js           # frontend logic
├── Dockerfile
├── requirements.txt
└── .env.example
```

---

## Getting Started

### 1. Clone the repository
```bash
git clone https://github.com/your-username/research-agent.git
cd research-agent
```

### 2. Create a virtual environment
```bash
python -m venv venv
venv\Scripts\activate        # Windows
source venv/bin/activate     # Mac/Linux
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Set up environment variables
Create a `.env` file in the root directory:
```
GOOGLE_API_KEY=your_gemini_api_key
TAVILY_API_KEY=your_tavily_api_key
LANGSMITH_API_KEY=your_langsmith_api_key
LANGCHAIN_TRACING_V2=true
LANGCHAIN_PROJECT=research-agent
```

Get your free API keys:
- Gemini → [aistudio.google.com](https://aistudio.google.com)
- Tavily → [tavily.com](https://tavily.com)
- LangSmith → [smith.langchain.com](https://smith.langchain.com)

### 5. Run the server
```bash
python -m uvicorn api.main:app --reload
```

### 6. Open in browser
```
http://127.0.0.1:8000
```

---

## Docker

### Build the image
```bash
docker build -t research-agent .
```

### Run the container
```bash
docker run -p 8000:8000 --env-file .env research-agent
```

---

## API

### POST /research
Submit a research question and receive a structured answer.

**Request:**
```json
{
  "question": "What are the best practices for deploying LLMs in production?"
}
```

**Response:**
```json
{
  "question": "What are the best practices for deploying LLMs in production?",
  "answer": "... structured research report ...",
  "revisions": 0
}
```

### GET /health
Returns the server status.

```json
{ "status": "ok" }
```

---

## Author

**AKROUR Mohammed**
- LinkedIn: [mohammed-akrour](https://linkedin.com/in/mohammed-akrour)
- Portfolio: [akrourmoh.github.io](https://akrourmoh.github.io)
- Email: akrourmohammedd@gmail.com
