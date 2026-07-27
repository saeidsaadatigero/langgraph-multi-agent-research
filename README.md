# 🦁 LangGraph Multi-Agent Research & Writing System

<div align="center">

[![Python](https://img.shields.io/badge/Python-3.12-blue.svg)](https://www.python.org/)
[![LangGraph](https://img.shields.io/badge/LangGraph-1.2.9-orange.svg)](https://langchain-ai.github.io/langgraph/)
[![LangChain](https://img.shields.io/badge/LangChain-1.3.14-green.svg)](https://www.langchain.com/)
[![DeepSeek](https://img.shields.io/badge/LLM-DeepSeek%20%7C%20OpenAI-purple.svg)](https://platform.deepseek.com/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Tests](https://img.shields.io/badge/Tests-5%2F5%20passed-brightgreen.svg)](tests/)

**Production-grade Multi-Agent AI system demonstrating advanced Agentic AI patterns with LangGraph, LangChain, and stateful orchestration.**

</div>

---

## 📋 Table of Contents

- [Overview](#-overview)
- [Architecture](#-architecture)
- [Agent Pipeline](#-agent-pipeline)
- [Key Features](#-key-features)
- [Why This Project Matters](#-why-this-project-matters)
- [Quick Start](#-quick-start)
- [Multi-Provider LLM Support](#-multi-provider-llm-support)
- [Example Output](#-example-output)
- [Project Structure](#-project-structure)
- [Testing](#-testing)
- [Use Cases](#-use-cases)
- [Skills Demonstrated](#-skills-demonstrated)
- [Roadmap](#-roadmap)
- [License](#-license)
- [Connect With Me](#-connect-with-me)

---

## 🎯 Overview

**LangGraph Multi-Agent Research & Writing System** is a production-grade demonstration of **Agentic AI patterns** — a 7-agent pipeline that researches any topic and generates publication-ready articles in **Bloomberg/Financial Times style**.

The system accepts a research topic and orchestrates seven specialized AI agents — each with a distinct role — to plan, research, analyze, write, review, revise, and finalize a comprehensive article. Built on **LangGraph's StateGraph** with **conditional routing**, **LLM-as-Judge evaluation**, and **stateful checkpointing**, it mirrors the multi-agent architectures used in enterprise AI deployments at companies like Mitratech, Bloomberg, and financial institutions.

**Why this exists:** This project bridges the gap between demo notebooks and production systems. It demonstrates patterns that are directly applicable to real-world Agentic AI workflows — from trading bots (PersianLionTrader) to legal document analysis, HR compliance systems, and enterprise RAG pipelines.

---

## 🏗️ Architecture

```
                         ┌──────────────────────┐
                         │      📋 PLANNER       │
                         │   (Research Director) │
                         │   Generates 5-7 deep   │
                         │   research questions   │
                         └──────────┬───────────┘
                                    │
                         ┌──────────▼───────────┐
                         │     🔍 RESEARCHER    │
                         │   (Data Analyst)      │
                         │   4-5 snippets per    │
                         │   question with stats │
                         └──────────┬───────────┘
                                    │
                         ┌──────────▼───────────┐
                         │     📊 ANALYST       │
                         │   (Managing Director) │
                         │   Boardroom-ready     │
                         │   research brief      │
                         └──────────┬───────────┘
                                    │
                         ┌──────────▼───────────┐
                         │      ✍️ WRITER       │
                         │   (Bloomberg/FT       │
                         │   Journalist)         │
                         │   800-1200 word       │
                         │   article             │
                         └──────────┬───────────┘
                                    │
                         ┌──────────▼───────────┐
                         │     🔎 REVIEWER       │
                         │   (Executive Editor)  │
                         │   5-criteria scoring  │
                         │   rubric              │
                         └───┬──────────┬───────┘
                             │          │
                    ┌────────▼──┐   ┌──▼──────────┐
                    │  APPROVED │   │   REVISE     │
                    │   (≥4.0)  │   │   (<4.0)     │
                    └────────┬──┘   └──┬──────────┘
                             │          │
                    ┌────────▼──┐   ┌──▼──────────┐
                    │ FINALIZER │   │   REVISER    │
                    │ (+Polish  │   │ (Systematic  │
                    │  +Key     │   │  Revision)   │
                    │  Takeaways)│   └──┬──────────┘
                    └────────┬──┘       │
                             │           │ (back to Reviewer)
                             ▼           │
                          ┌──────┐       │
                          │ END  │◄──────┘
                          └──────┘
```

**Safety Guardrail:** After `max_revisions` (default: 2), the pipeline force-finalizes to prevent infinite revision loops — a critical production pattern.

---

## 🤖 Agent Pipeline

| # | Agent | Role | Real-World Analogy | Output |
|---|-------|------|-------------------|--------|
| 1 | **Planner** | Research Director | Assigns journalists to angles | 5-7 focused questions |
| 2 | **Researcher** | Data Analyst | Pulls Bloomberg Terminal data | 4-5 factual snippets per question |
| 3 | **Analyst** | Managing Director | Synthesizes for executives | Boardroom-ready brief (6 sections) |
| 4 | **Writer** | Financial Journalist | Bloomberg/FT writer | 800-1200 word article |
| 5 | **Reviewer** | Executive Editor | Strict quality gate | Scored rubric + revision notes |
| 6 | **Reviser** | Pulitzer Editor | Addresses every issue | Fully revised article |
| 7 | **Finalizer** | Copy Editor | Pre-publication polish | Final + Key Takeaways box |

---

## ✨ Key Features

### 🧠 Advanced AI Patterns
- **LLM-as-Judge**: Reviewer agent uses a 5-criteria scoring rubric (Factual Rigor, Structure, Technical Accuracy, Balance, Writing Quality) — only articles scoring ≥4.0/5.0 are approved
- **Conditional Routing**: `route_after_reviewer()` implements business logic that decides: approve → finalize, reject → revise, max_revisions → force-stop
- **Stateful Orchestration**: `AgentState` (TypedDict) flows through all agents with `MemorySaver` checkpointing for audit trails and resume capability

### 🏢 Production-Grade Design
- **Multi-Provider LLM**: Switch between DeepSeek and OpenAI via `LLM_PROVIDER` env var — factory pattern enables easy addition of Anthropic, Groq, or local models
- **Safety Guardrails**: `max_revisions` prevents infinite loops; graceful error handling with fallback plans
- **Domain-Aware Prompts**: Planner adapts question style based on topic domain (trading → quantitative, Django → architectural, AI → technical)

### 📝 Professional Output Quality
- **Bloomberg/FT Writing Style**: Strong lede paragraphs, data-driven narrative, balanced perspective
- **Source Attribution**: Every claim backed by synthesized sources with inline citations
- **Key Takeaways Box**: Finalizer adds executive summary with 3 bullet points

### 🧪 Testing & Quality
- **5 pytest tests**: Graph compilation, node presence, full pipeline E2E, safety guardrail verification
- **Mock-free integration tests**: Tests invoke the actual LLM pipeline and validate output structure

---

## 💼 Why This Project Matters

This project demonstrates the exact skills required in senior AI/ML engineering roles:

| Skill | Where It's Demonstrated |
|-------|------------------------|
| **Agent Orchestration** | 7-agent LangGraph StateGraph with conditional routing |
| **LangGraph/LangChain** | StateGraph, MemorySaver, ChatDeepSeek, ChatOpenAI |
| **Multi-Agent Systems** | Hierarchical agents with role specialization |
| **LLM-as-Judge** | Reviewer with 5-criteria scoring rubric |
| **RAG & Retrieval** | Researcher simulates search with attribution (Tavily-ready architecture) |
| **Prompt Engineering** | 7 domain-aware, structured-output prompts |
| **State Management** | TypedDict state flowing through graph with checkpointing |
| **Safety Guardrails** | max_revisions, error handling, fallback strategies |
| **Production Python** | Type hints, factory pattern, env-based config |
| **Testing** | pytest with E2E integration tests |

---

## 🚀 Quick Start

### Prerequisites
- Python 3.11+
- DeepSeek API key ([get one here](https://platform.deepseek.com/api_keys)) **or** OpenAI API key ([get one here](https://platform.openai.com/api-keys))

### Installation

```bash
# Clone the repository
git clone https://github.com/saeidsaadatigero/langgraph-multi-agent-research.git
cd langgraph-multi-agent-research

# Create and activate virtual environment
python -m venv .venv

# Windows
.venv\Scripts\activate

# Linux/Mac
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### Configuration

```bash
# Copy the example environment file
cp .env.example .env

# Edit .env with your API keys
```

Example `.env`:
```env
# Choose your LLM provider: deepseek or openai
LLM_PROVIDER=deepseek

# DeepSeek API Key
DEEPSEEK_API_KEY=sk-your-key-here

# OpenAI API Key (only needed if LLM_PROVIDER=openai)
OPENAI_API_KEY=sk-your-key-here
```

### Run

```bash
python main.py
```

Enter any research topic when prompted, for example:
```
The Future of Algorithmic Trading: How AI-Powered Multi-Agent Systems Are Transforming Financial Markets
```

The pipeline runs for 2-5 minutes and outputs a publication-ready article.

---

## 🔄 Multi-Provider LLM Support

Switch between LLM providers by changing one line in `.env`:

```env
# Use DeepSeek
LLM_PROVIDER=deepseek

# Use OpenAI (gpt-4o-mini)
LLM_PROVIDER=openai
```

| Provider | Model | Input Cost | Output Cost | Best For |
|----------|-------|------------|-------------|----------|
| DeepSeek | deepseek-chat | $0.27/M tokens | $1.10/M tokens | Persian content, demo projects |
| OpenAI | gpt-4o-mini | $0.15/M tokens | $0.60/M tokens | Cost-effective, fast |

**Architecture Note:** The LLM is created via a factory function (`_create_llm()`) that reads `LLM_PROVIDER` from the environment. Adding a new provider (Anthropic, Groq, local Ollama) requires only adding one `elif` branch — no changes to agent nodes.

---

## 📰 Example Output

**Input Topic:**
> *"The Future of Algorithmic Trading: How AI-Powered Multi-Agent Systems Like PersianLionTrader Are Transforming Financial Markets"*

**Output:** A 1,100-word article published on LinkedIn:  
🔗 [The Machine Council: How Multi-Agent AI Systems Are Reshaping Algorithmic Trading](https://www.linkedin.com/pulse/machine-council-how-multi-agent-ai-systems-reshaping-saadatigero-gpsif/)

**Output Quality Highlights:**
- ✅ Strong lede with specific statistic (34.2% annualized return)
- ✅ Architecture deep-dive: all 5 PersianLionTrader agents explained
- ✅ "By the Numbers" section with comparative metrics
- ✅ Honest risk disclosure: "unaudited backtests," "not peer-reviewed"
- ✅ Expert quote synthesis with source attribution
- ✅ Key Takeaways box for executive readers

---

## 📁 Project Structure

```
langgraph-multi-agent-research/
├── src/
│   ├── __init__.py              # Package init
│   ├── state.py                 # AgentState TypedDict definition
│   └── research_graph.py        # Graph definition (7 agents + routing)
├── tests/
│   ├── __init__.py              # Test package init
│   └── test_research_graph.py   # 5 pytest tests (compilation + E2E)
├── main.py                      # CLI entry point
├── requirements.txt             # Python dependencies
├── .env.example                 # Environment variables template
├── .gitignore                   # Git ignore rules
├── LICENSE                      # MIT License
└── README.md                    # You are here
```

---

## 🧪 Testing

```bash
# Run all tests
python -m pytest tests/test_research_graph.py -v

# Expected output:
# test_graph_builds_successfully PASSED
# test_graph_has_all_expected_nodes PASSED
# test_graph_has_entry_point PASSED
# test_full_pipeline_invocation PASSED
# test_pipeline_safety_stops_at_max_revisions PASSED
```

**Test Coverage:**
- **Graph Compilation** (3 tests): Verifies the StateGraph builds and has all 7 agent nodes
- **Integration/E2E** (2 tests): Full pipeline invocation with real LLM calls, validates output structure and safety guardrail

---

## 🎯 Use Cases

This architecture pattern applies to many enterprise AI workflows:

| Domain | Application | Agents |
|--------|------------|--------|
| **Finance** | Research reports, market analysis | Planner, Research, Risk Assessment, Writer, Compliance Review |
| **Legal** | Contract analysis, compliance docs | Clause Extractor, Risk Analyzer, Legal Writer, Partner Review |
| **HR** | Policy documents, training materials | Policy Researcher, Legal Check, Content Writer, HR Director Review |
| **Software** | Technical documentation, architecture decisions | Spec Analyzer, Code Researcher, Docs Writer, Architect Review |
| **Education** | Course materials, study guides | Curriculum Designer, Content Researcher, Lesson Writer, Peer Reviewer |

---

## 🛠️ Skills Demonstrated

<div align="center">

| Category | Technologies & Patterns |
|----------|------------------------|
| **AI/ML** | LangGraph, LangChain, DeepSeek, OpenAI, LLM-as-Judge |
| **Architecture** | Multi-Agent Systems, StateGraph, Conditional Routing, State Management |
| **Patterns** | Factory Pattern, Dependency Injection, Repository Pattern |
| **Python** | Type Hints, TypedDict, ast.literal_eval, env-based config |
| **Testing** | pytest, E2E Integration Tests, Safety Guardrail Verification |
| **DevOps** | Git, Conventional Commits, .env configuration |
| **Writing** | Technical Documentation, README, LinkedIn Articles |

</div>

---

## 🗺️ Roadmap

- [x] 7-agent LangGraph pipeline
- [x] Multi-provider LLM support (DeepSeek + OpenAI)
- [x] LLM-as-Judge with scored rubric
- [x] Safety guardrails (max_revisions)
- [x] pytest suite (5 tests)
- [x] LinkedIn article publication
- [ ] FastAPI REST endpoint
- [ ] Docker containerization
- [ ] LangFuse observability & tracing
- [ ] Tavily Search API integration (replace simulated search)
- [ ] Streaming output (SSE)
- [ ] Hybrid provider per node (e.g., GPT-4 for Reviewer, DeepSeek for Researcher)

---

## 📄 License

This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.

---

## 🔗 Connect With Me

<div align="center">

[![LinkedIn](https://img.shields.io/badge/LinkedIn-Connect-blue?style=for-the-badge&logo=linkedin)](https://www.linkedin.com/in/saeid-saadatigero/)
[![GitHub](https://img.shields.io/badge/GitHub-Follow-black?style=for-the-badge&logo=github)](https://github.com/saeidsaadatigero)
[![Email](https://img.shields.io/badge/Email-Contact-red?style=for-the-badge&logo=gmail)](mailto:saeidsaadatigero@gmail.com)

**Saeid Saadatigero**  
Senior Backend Engineer (Django) | AI/ML Engineer | Agentic AI Systems

</div>

---

<div align="center">

**🦁 Built with LangGraph, LangChain, and DeepSeek**

*"The most important algorithm may not be the one that trades fastest, but the one that governs the conversation between machines."*

</div>