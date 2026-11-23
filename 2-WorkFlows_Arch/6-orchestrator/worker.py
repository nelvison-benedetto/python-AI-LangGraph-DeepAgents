
from typing import Annotated, List, TypedDict
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages

from langchain_openai import ChatOpenAI
from langgraph.types import Send
from operator import add
from pydantic import BaseModel, Field


class OverallState(TypedDict):
    research_topic: str
    sources: List[str]
    worker_findings: Annotated[List[dict], add]
    final_report: str

class WorkerState(TypedDict):
    source: str
    worker_id: int
    reseach_topic: str


class ResearchPlan(BaseModel):
    sources: List[str] = Field(
        description="List of specific research sources/aspects to investigate"
        max_length=5
    )
    reasoning: str = Field(
        description="brief explanation of why these sources where chosen"
    )

llm = ChatOpenAI(model="gpt-4o")


def plan_research(state=OverallState)->OverallState:
    print("\n"+"="*10)
    print("orchestrator: planning research strategy")
    print("="*10)
    print(f"topic: {state['research_topic']}\n")
    planner_llm = llm.with_structured_output(ResearchPlan)
    prompt=f"""
    you are a research strategist plannin a comprehensive investigation.
    research topi: {state['research_topic']}
    critical instruction: generate between 3-5 specifi research sources or aspects to investigate.
    do not generate more than 5 sources.
    each source should be:
    - specific and focused on a distinct aspect
    - relevant to the overall topic
    - complementary to other sources (minimal overalap)
    - concrete enough to guide targeted research
    examples of good sources: 
    - "clinical trial results and efficacy data"
    - "economic impact and cost-benefit analysis"
    - "regulatory framework and compliance requirements"
    - "patient outcomes and quality of life metrics"
    - "industry adoption rates and market trends"
    generate sources that will provide comprehensive coverage of the topic.
    """
    



