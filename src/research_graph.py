# src/research_graph.py
"""
LangGraph Multi-Agent Research & Writing System — Graph Definition.

Architecture Pattern: StateGraph with 7 specialized agents (nodes)
connected through conditional routing (edges).

Optimization v2.0:
- Writer: Bloomberg/Financial Times/ForexFactory hybrid style
- Reviewer: Strict fact-checking with numerical claim verification
- Researcher: Real-world statistics even in simulated mode
- Planner: Smart question generation for any domain (trading, Django, AI)
- Generic: Works for any topic — trading, backend engineering, AI/ML
"""

import ast
import os
from typing import Literal

from dotenv import load_dotenv
from langchain_deepseek import ChatDeepSeek
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import StateGraph, END

from src.state import AgentState

load_dotenv()


# ── LLM Configuration (Multi-Provider) ────────────────────

def _create_llm():
    """
    Factory function: Create LLM instance based on LLM_PROVIDER env var.
    
    Supported providers:
    - deepseek: ChatDeepSeek (deepseek-chat model)
    - openai: ChatOpenAI (gpt-4o-mini model, cost-effective default)
    
    Production Note: In a full production system, this factory would be
    a proper Provider abstract class with implementations for each provider,
    injected via dependency injection. This module-level singleton is
    acceptable for the demo scope.
    """
    provider = os.getenv("LLM_PROVIDER", "deepseek").lower().strip()
    
    if provider == "deepseek":
        api_key = os.getenv("DEEPSEEK_API_KEY")
        if not api_key or api_key == "sk-your-key-here":
            raise ValueError(
                "DEEPSEEK_API_KEY not configured. "
                "Set it in your .env file or switch LLM_PROVIDER to openai."
            )
        print("  🤖 Using DeepSeek (deepseek-chat)")
        return ChatDeepSeek(
            model="deepseek-chat",
            api_key=api_key,
            temperature=0.3,
        )
    
    elif provider == "openai":
        from langchain_openai import ChatOpenAI
        
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key or api_key == "sk-your-key-here":
            raise ValueError(
                "OPENAI_API_KEY not configured. "
                "Set it in your .env file or switch LLM_PROVIDER to deepseek."
            )
        print("  🤖 Using OpenAI (gpt-4o-mini)")
        return ChatOpenAI(
            model="gpt-4o-mini",  # Cost-effective, fast, good quality
            api_key=api_key,
            temperature=0.3,
        )
    
    else:
        raise ValueError(
            f"Unknown LLM_PROVIDER: '{provider}'. "
            "Supported providers: deepseek, openai"
        )


# Module-level instance (acceptable for demo; use factory injection in production)
llm = _create_llm()


# ── Agent Node: Planner (سردبیر) ──────────────────────────

def planner_node(state: AgentState) -> AgentState:
    """
    Break the research topic into 5-7 focused, answerable questions.

    Optimized v2: Domain-aware — adapts question style based on topic
    (trading → quantitative, Django → architectural, AI → technical).
    """
    prompt = f"""You are a senior research director at a top-tier financial and technology publication (Bloomberg, Financial Times, TechCrunch).

Your task: Break the following topic into 5-7 specific, deeply focused research questions. Each question should target a distinct angle that, when answered, produces a comprehensive, publication-ready article.

Topic: {state["topic"]}

Guidelines for question generation (adapt to the domain of the topic):
- If the topic is about **trading/finance**: Include questions about P&L metrics, risk management architecture, regulatory implications, technology stack, and real-world performance data.
- If the topic is about **backend engineering/Django**: Include questions about architecture patterns, scalability benchmarks, production deployment, security considerations, and comparison with alternatives.
- If the topic is about **AI/ML/LLMs**: Include questions about model architecture, training methodology, evaluation metrics, production inference challenges, cost analysis, and ethical considerations.
- Regardless of domain: ALWAYS include at least one question about **real-world statistics**, one about **competitive landscape/comparison**, and one about **future outlook**.

CRITICAL: Return ONLY a valid Python list of strings. Example format:
["Question 1 about specific aspect", "Question 2 with quantitative angle", "Question 3 about competitive comparison", "Question 4 about future outlook", "Question 5 about technical implementation"]
Do NOT include any other text, markdown fences, or explanations. Output raw Python list only."""

    response = llm.invoke(prompt)

    try:
        content = response.content.strip()
        if content.startswith("```"):
            content = content.split("```")[1]
            if content.startswith("python"):
                content = content[6:]
            content = content.strip()
        plan = ast.literal_eval(content)
        if not isinstance(plan, list) or len(plan) == 0:
            raise ValueError("Parsed plan is not a valid list")
    except Exception as e:
        print(f"  ⚠️  Planner parsing failed ({e}), using fallback plan.")
        plan = [f"Comprehensive analysis of: {state['topic']}"]

    return {**state, "plan": plan}


# ── Agent Node: Researcher (محقق) ─────────────────────────

def researcher_node(state: AgentState) -> AgentState:
    """
    Simulate web search with real-world statistics and specific data points.

    Optimized v2: Even in simulated mode, generates realistic statistics,
    company names, timeline data, and industry-specific metrics.
    """
    results = []
    plan_questions = state.get("plan", [])

    for i, question in enumerate(plan_questions[:5]):  # Up to 5 for depth
        print(f"  🔍 Researching [{i+1}/{min(len(plan_questions), 5)}]: {question[:80]}...")

        prompt = f"""You are a specialized financial and technology research analyst with access to premium databases (Bloomberg Terminal, Crunchbase, IEEE Xplore, arXiv).

For the query below, generate 4-5 deeply researched, realistic search result snippets. CRITICAL REQUIREMENTS:
- Include **specific numbers, statistics, or percentages** where applicable (e.g., "According to a 2025 JPMorgan report, 67% of institutional traders...")
- Reference **real companies, products, or frameworks** (e.g., "MetaTrader 5", "DeepSeek-V3", "Django 5.1", "LangGraph", "Bloomberg")
- Include **timeline data** where relevant (e.g., "Between 2020-2025, the algo-trading market grew from...")
- Present **contrasting viewpoints** if they exist (e.g., "While proponents argue X, critics like [expert name] point to Y")
- Each snippet should be 2-4 sentences with journalistic quality

Query: {question}

Return the snippets as a numbered list with each entry being a self-contained, citation-ready paragraph."""

        response = llm.invoke(prompt)
        results.append(f"### Research Findings: {question}\n{response.content}")

    return {**state, "search_results": results}


# ── Agent Node: Analyst (تحلیلگر) ─────────────────────────

def analyst_node(state: AgentState) -> AgentState:
    """
    Synthesize research into a structured analysis brief.

    Optimized v2: Produces executive-style brief with quantitative
    highlights, SWOT analysis, and actionable insights.
    """
    search_text = "\n\n".join(state.get("search_results", []))

    max_chars = 8000  # Increased for deeper analysis
    if len(search_text) > max_chars:
        search_text = search_text[:max_chars] + "\n[... additional research truncated for brevity]"

    prompt = f"""You are a Managing Director of Research at a premier financial and technology intelligence firm (like Gartner or Bloomberg Intelligence).

Using the search results below, produce a comprehensive, boardroom-ready research brief. Structure your response EXACTLY as follows:

---

## Executive Summary
[3-4 sentences: the single most important takeaway, supported by the strongest statistic from the research]

## Key Quantitative Findings
- [Finding 1 with specific number/percentage and source attribution]
- [Finding 2 with specific number/percentage and source attribution]
- [Finding 3 with specific number/percentage and source attribution]
- [Finding 4: market size, growth rate, or adoption metric]

## Competitive Landscape & Comparisons
[Compare the main approaches, tools, or players mentioned in the research. Use a comparative framework — features, performance, cost, adoption.]

## Technical Deep-Dive
[Detailed analysis of the underlying technology, architecture, or methodology. Include specific technical terms, frameworks, and architectural decisions.]

## Risks, Challenges & Contrarian Views
[What could go wrong? What do skeptics say? Include regulatory, technical, and market risks.]

## Strategic Implications & Future Outlook
[What does this mean for the industry? 3-5 year horizon. Actionable insights for practitioners.]

---

Topic: {state["topic"]}

Research Data:
{search_text}

Write your complete analysis brief now. Maintain boardroom quality — this goes to senior executives and technical leads."""

    response = llm.invoke(prompt)
    return {**state, "research_summary": response.content}


# ── Agent Node: Writer (نویسنده) ──────────────────────────

def writer_node(state: AgentState) -> AgentState:
    """
    Write a publication-ready article in Bloomberg/Financial Times style.

    Optimized v2: Professional financial journalism style with:
    - Strong lede paragraph with a hook
    - Data-driven narrative
    - Expert sourcing (from research)
    - Balanced perspective
    - Professional markdown formatting
    """
    summary = state.get("research_summary", "")

    max_chars = 10000  # Full context for rich article
    if len(summary) > max_chars:
        summary = summary[:max_chars] + "\n[... full brief available in appendix]"

    prompt = f"""You are a senior financial and technology journalist writing for Bloomberg, Financial Times, and ForexFactory. Your articles are known for:
- **Strong, data-driven lede paragraphs** that hook readers immediately
- **Rigorous sourcing**: Every major claim backed by a specific statistic, study, or expert
- **Balanced analysis**: Present both bullish and bearish perspectives
- **Technical depth**: You understand the technology well enough to explain it clearly
- **Professional yet accessible tone**: Sophisticated but not academic

Write a comprehensive, publication-ready article based on the research brief below.

## Article Structure (REQUIRED):

### Title
[A compelling, specific title. Use patterns like:
- "How [Technology] Is [Transforming/Disrupting] [Industry]"
- "Inside [Company/Project]: The [Adjective] [Technology] That [Achievement]"
- "[Number] Ways [Topic] Is Changing [Domain]"]

### Lede Paragraph (3-4 sentences)
[Start with a specific, surprising statistic or a vivid scene. Draw the reader in. Example: "When PersianLionTrader executed its first fully autonomous trade on a Tuesday morning in March, it didn't just place an order — it consulted four AI agents, analyzed 27 technical indicators, cross-referenced breaking news, and calculated position size based on real-time volatility. The entire process took 1.2 seconds."]

### Body Sections (use ## for main sections, ### for subsections):
1. **The Big Picture** — Industry context, market size, why this matters now
2. **How It Works** — Technical architecture explained clearly with specific technologies named
3. **By the Numbers** — Dedicated section with key statistics, charts-described-in-text, performance metrics
4. **The Competitive Landscape** — Who else is doing this? How does this compare?
5. **Risks and Challenges** — Honest assessment of limitations, regulatory concerns, technical hurdles
6. **What's Next** — 3-5 year outlook, emerging trends, predictions

### Conclusion
[2-3 paragraphs synthesizing the key argument and leaving the reader with a forward-looking insight.]

## Writing Guidelines:
- **Word count**: 800-1200 words (comprehensive but focused)
- **Citations**: Reference sources naturally ("According to a 2025 JPMorgan report...", "As noted by [expert/company]...")
- **Quotes**: Include at least one "expert quote" (can be synthesized from research)
- **Data visualization hints**: Describe what a chart would show ("A line chart of adoption rates would reveal...")
- **NO generic filler**: Every paragraph must add new information or insight
- **NO markdown code blocks**: Use professional formatting only (headings, bold, italic, lists)

Topic: {state["topic"]}

Research Brief:
{summary}

Write the complete, polished article now. Output ONLY the article in Markdown format — no meta-commentary, no "Here's the article", just the article itself."""

    response = llm.invoke(prompt)
    return {**state, "draft": response.content}


# ── Agent Node: Reviewer (ویراستار) ───────────────────────

def reviewer_node(state: AgentState) -> AgentState:
    """
    Strict editorial review with fact-checking and numerical claim verification.

    Optimized v2: Aggressive quality control — checks for:
    - Unsubstantiated numerical claims
    - Logical contradictions
    - Missing citations
    - Structural weaknesses
    - Tone consistency
    """
    draft = state.get("draft", "")

    max_chars = 10000
    if len(draft) > max_chars:
        draft = draft[:max_chars] + "\n[... article truncated for review]"

    prompt = f"""You are the Executive Editor at Bloomberg, known for your ruthless quality standards. Your reputation depends on publishing only flawless articles.

Review the article draft below against this STRICT quality rubric. You are NOT being nice — you are being accurate.

## Quality Rubric (Score each 1-5, where 5 is publication-ready):

### 1. Factual Rigor & Attribution
- Are numerical claims backed by specific sources?
- Are statistics plausible and contextually appropriate?
- Are claims like "67% of traders..." attributed to a source?
- Score: [1-5]

### 2. Structural Excellence
- Does the lede hook the reader with a specific, compelling detail?
- Does each section fulfill its promised purpose?
- Is there a logical flow from context → detail → analysis → outlook?
- Score: [1-5]

### 3. Technical Accuracy
- Are technologies, frameworks, and methodologies correctly described?
- Would a domain expert find errors or oversimplifications?
- Are acronyms and technical terms used correctly?
- Score: [1-5]

### 4. Balance & Objectivity
- Are both optimistic and skeptical perspectives presented?
- Does the article acknowledge limitations and risks honestly?
- Is there any promotional/hype language that undermines credibility?
- Score: [1-5]

### 5. Writing Quality
- Is the prose clear, engaging, and professional?
- Are there any clichés, jargon without explanation, or awkward constructions?
- Would this meet Bloomberg/FT publication standards?
- Score: [1-5]

## Decision Matrix:
- **APPROVED**: Average score ≥ 4.0 AND no individual score < 3
- **REVISE**: Average score < 4.0 OR any individual score < 3

## Required Output Format:

If APPROVED, respond with EXACTLY:
APPROVED
[One sentence explaining why — reference the strongest aspect]

If REVISE, respond with EXACTLY:
REVISE
## Revision Requirements
[Bullet list of SPECIFIC, ACTIONABLE changes. For each issue:]
- **Location**: [Which section/paragraph]
- **Issue**: [What's wrong — be precise]
- **Fix**: [Exactly what to do — "Add a citation for the 67% claim", "Rewrite the lede to start with the $4.2B market size statistic", "Remove the promotional language about DeepSeek being 'revolutionary' without evidence"]

Article Draft:
{draft}

Your review (APPROVED or REVISE with detailed requirements):"""

    response = llm.invoke(prompt)
    decision_text = response.content.strip()

    if decision_text.upper().startswith("APPROVED"):
        return {**state, "feedback": None, "approved": True}
    else:
        feedback = decision_text
        if decision_text.upper().startswith("REVISE:"):
            feedback = decision_text[7:].strip()
        elif decision_text.upper().startswith("REVISE"):
            feedback = decision_text[6:].strip()
        return {**state, "feedback": feedback, "approved": False}


# ── Agent Node: Reviser (بازبین) ──────────────────────────

def reviser_node(state: AgentState) -> AgentState:
    """
    Revise the draft based on strict reviewer feedback.

    Optimized v2: Addresses each revision point systematically
    and ensures the revised article meets publication standards.
    """
    prompt = f"""You are a Pulitzer-winning editor tasked with revising an article to meet Bloomberg/FT publication standards.

Below is the original draft and the editor's revision requirements. Your job:
1. Address EVERY revision point systematically
2. Preserve what was good in the original
3. Ensure the revised version is strictly better — more factual, better structured, more engaging
4. Maintain the professional financial journalism tone throughout

Editor's Revision Requirements:
{state["feedback"]}

Original Draft:
{state["draft"][:8000]}

Write the COMPLETE revised article now (not just the changed sections — the full article).
Output ONLY the complete, revised article in Markdown format."""

    response = llm.invoke(prompt)
    new_revision_count = state.get("revision_count", 0) + 1

    return {
        **state,
        "draft": response.content,
        "feedback": None,
        "revision_count": new_revision_count,
    }


# ── Agent Node: Finalizer (نهایی‌ساز) ──────────────────────

def finalizer_node(state: AgentState) -> AgentState:
    """
    Finalize the pipeline: prepare the polished, publication-ready output.

    Adds final polish: consistent formatting, metadata-ready structure.
    """
    draft = state.get("draft", "")

    prompt = f"""You are a copy editor at Bloomberg doing the final pass before publication.

Perform these final polish tasks on the article below:
1. Ensure consistent Markdown formatting throughout
2. Fix any minor typos, awkward phrasing, or punctuation issues
3. Ensure section headings follow a consistent hierarchy
4. Add a brief "Key Takeaways" box at the very beginning (after the title, before the lede) with 3 bullet points
5. Ensure the article ends with a strong, forward-looking closing paragraph

CRITICAL: Do NOT rewrite the article. Only polish and add the Key Takeaways box.

Article:
{draft[:10000]}

Output the polished, publication-ready article now:"""

    response = llm.invoke(prompt)
    return {**state, "final_output": response.content}


# ── Routing Logic (مسیریاب شرطی) ──────────────────────────

def route_after_reviewer(state: AgentState) -> Literal["reviser", "finalizer"]:
    """
    Conditional edge: Decide the next step after review.

    Safety: Force-finalize after max_revisions to prevent infinite loops.
    """
    if state.get("approved", False):
        return "finalizer"

    max_rev = state.get("max_revisions", 2)
    rev_count = state.get("revision_count", 0)
    if rev_count >= max_rev:
        print(f"  ⚠️  Max revisions ({max_rev}) reached — force finalizing.")
        return "finalizer"

    return "reviser"


# ── Graph Construction (ساخت گراف) ─────────────────────────

def build_research_graph() -> StateGraph:
    """
    Build and compile the LangGraph StateGraph.

    Graph Topology v2:
    ┌─────────┐    ┌───────────┐    ┌──────────┐    ┌────────┐
    │ Planner │───▶│ Researcher│───▶│ Analyst  │───▶│ Writer │
    │(5-7 Qs) │    │(4-5 snips)│    │(Boardroom)│    │(Bloom.)│
    └─────────┘    └───────────┘    └──────────┘    └───┬────┘
                                                        │
                                            ┌───────────▼──────────┐
                                            │  Reviewer (Strict)    │
                                            │  (Scored rubric)      │
                                            └───┬──────────┬───────┘
                                                │          │
                                          APPROVED      REVISE
                                           (≥4.0)       (<4.0)
                                                │          │
                                        ┌───────▼──┐  ┌───▼───────┐
                                        │Finalizer │  │  Reviser  │
                                        │(+Polish) │  │(Systematic)│
                                        │  (END)   │  └───┬───────┘
                                        └──────────┘      │
                                                     (back to Reviewer)
    """
    graph = StateGraph(AgentState)

    # Add nodes
    graph.add_node("planner", planner_node)
    graph.add_node("researcher", researcher_node)
    graph.add_node("analyst", analyst_node)
    graph.add_node("writer", writer_node)
    graph.add_node("reviewer", reviewer_node)
    graph.add_node("reviser", reviser_node)
    graph.add_node("finalizer", finalizer_node)

    # Add edges
    graph.set_entry_point("planner")
    graph.add_edge("planner", "researcher")
    graph.add_edge("researcher", "analyst")
    graph.add_edge("analyst", "writer")
    graph.add_edge("writer", "reviewer")

    # Conditional branching
    graph.add_conditional_edges(
        "reviewer",
        route_after_reviewer,
        {
            "reviser": "reviser",
            "finalizer": "finalizer",
        },
    )
    graph.add_edge("reviser", "reviewer")
    graph.add_edge("finalizer", END)

    # Compile with checkpointing
    memory = MemorySaver()
    compiled_graph = graph.compile(checkpointer=memory)

    return compiled_graph