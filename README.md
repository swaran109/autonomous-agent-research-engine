# Autonomous Multi-Agent Enterprise Research Engine

An asynchronous multi-agent pipeline built with **LangGraph**, **FastAPI**, and **Groq Cloud LLM** (`qwen/qwen3.8-27b`) for automated web research synthesis and strategic report drafting.

---

## Architecture Overview

```text
[User Request] 
      │
      ▼
[FastAPI REST API] 
      │
      ▼
[LangGraph StateGraph]
      │
      ├──▶ Node 1: Web Searcher (DuckDuckGo integration & contextual retrieval)
      │
      └──▶ Node 2: Executive Synthesizer (Groq LLM structured markdown synthesis)
      │
      ▼
[Final Executive Report Response]