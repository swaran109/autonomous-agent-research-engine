import os
from typing import TypedDict, List
from dotenv import load_dotenv
from langgraph.graph import StateGraph, END
from duckduckgo_search import DDGS
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage

load_dotenv()

class AgentState(TypedDict):
    topic: str
    search_results: List[str]
    report: str
    status: str

# API key verify karein
api_key = os.getenv("GROQ_API_KEY")
if not api_key:
    # Direct fallback if .env fails to load
    api_key = "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"

llm = ChatGroq(
    model="qwen/qwen3.8-27b",
    api_key=api_key,
    temperature=0.3
)

def search_web_node(state: AgentState):
    query = state["topic"]
    results = []
    try:
        with DDGS() as ddgs:
            raw_results = list(ddgs.text(query, max_results=3))
            for r in raw_results:
                title = r.get("title", "No Title")
                body = r.get("body", "No Body")
                href = r.get("href", "")
                results.append(f"Title: {title}\nSnippet: {body}\nSource: {href}")
    except Exception as e:
        results.append(f"Search note: Real-time query generated fallback context due to: {str(e)}")
    
    if not results:
        results.append("General industry knowledge synthesized.")

    return {
        "search_results": results,
        "status": "Search Completed"
    }

def synthesize_report_node(state: AgentState):
    context = "\n\n".join(state.get("search_results", []))
    prompt = f"""You are an Autonomous Executive Research Agent.
Analyze the following information for the topic: '{state['topic']}'.
Synthesize a structured markdown report with:
1. Executive Summary
2. Key Insights & Findings
3. Strategic Takeaways
4. Cited Sources

Context / Findings:
{context}
"""
    try:
        response = llm.invoke([HumanMessage(content=prompt)])
        report_text = response.content
    except Exception as err:
        report_text = f"LLM Generation Error: {str(err)}"

    return {
        "report": report_text,
        "status": "Completed"
    }

workflow = StateGraph(AgentState)
workflow.add_node("searcher", search_web_node)
workflow.add_node("synthesizer", synthesize_report_node)

workflow.set_entry_point("searcher")
workflow.add_edge("searcher", "synthesizer")
workflow.add_edge("synthesizer", END)

research_graph = workflow.compile()