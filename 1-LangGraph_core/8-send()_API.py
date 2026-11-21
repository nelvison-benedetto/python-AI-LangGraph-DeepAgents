
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from typing import TypedDict, List, Annotated

from operator import add
from langgraph.types import Send


class OverallState(TypedDict):
    topic: str
    subtopics: List[str]
    research_results: Annotated[List[str], add]
    final_report: str

class ResearchState(TypedDict):
    subtopic: str
    research_results: List[str]

def generate_subtopics(state:OverallState):
    topic=state['topic']
    subtopics= [
        f"{topic} - history",
        f"{topic} - current trends",
        f"{topic} - future outlook",
    ]
    return {
        "subtopics": subtopics
    }

def research_subtopic(state:ResearchState):
    subtopic= state['subtopic']
    result = f"research finding on '{subtopic}': [detailed analysis, data, insights, ...]"
    return {
        "research_results": [result]
    }

def compile_report(state:OverallState):
    results = state[research_results]
    report = "="*10
    report += "COMPRHENSIVE RESEARCH REPORT\n"
    report += "=" * 50 + "\n"
    for i, result in enumerate(results, 1):
        report += f"{i}. {result}\n\n"
    return {
        "final_report": report
    }    






