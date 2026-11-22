
from typing import TypedDict, List, Annotated
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages

from langchain_openai import ChatOpenAI


class ContentState(TypedDict):
    topic: str
    requirements: str
    draft: str
    fact_check_results: str
    improved_content: str
    final_draft: str

llm = ChatOpenAI(model="gpt-4o")

def generate_draft(state: ContentState)->ContentState:
    prompt= f"""
        write a 200-word blog post about {state['topic']}
        requirements: {state['requirements']}
        focus on creting engaging, informative content
    """
    draft = llm.invoke(prompt).content
    print("===STEP 1: draft generated ===")
    print (draft[:150]+"...\n")
    return {
        "draft": draft
    }


def fact_check(state: ContentState)->ContentState:
    prompt=f"""
    review the following blog post draft for factual accuracy and consistency: {state['draft']} identity: 
    1. any factual claims that seem questionable
    2. internal inconsistencies
    3. statements that need citations
    provide a brief report.
    """

    fact_check_results = llm.invoke(prompt).content
    print("===STEP 2: fact check complete ===")
    print (fact_check_results[:150]+"...\n")
    return {
        "fact_check_results": fact_check_results
    }


def improve_content(state:ContentState)->ContentState:
    prompt= f"""
    here is a blog post draft:
    {state['draft']}
    here is feedback from fact-checking
    {state['fact_check_results']}
    revise the blog post to address the feedback while maintaining engaging writing. keep it around 200 worlds.
    """
    improved = llm.invoke(prompt).content
    print("===STEP 3: content improved ===")
    print (improved[:150]+"...\n")
    return {
        "improved_content": improved
    }


def format_output(state: ContentState)->ContentState:
    prompt= f"""
    format the following blog post for the web publication:
    {state['improved_content']}
    add:
    - an engaging title wrapped in <h1> tags
    - subheadings where appropriate with <h2> tags
    - paragraph tags <p>
    - a meta description (1-2 sentences)
    output the formatted html.
    """
    final = llm.invoke(prompt).content
    print("===STEP 4: formatted for publication ===")
    print (final[:200]+"...\n")
    return {
        "final_draft": final
    }


builder = StateGraph(ContentState)
builder.add_node(generate_draft)
builder.add_node(fact_check)
builder.add_node(improve_content)
builder.add_node(format_output)

builder.add_edge(START, "generate_draft")
builder.add_edge("generate_draft", "fact_check")
builder.add_edge("fact_check", "improve_content")
builder.add_edge("improve_content", "format_output")
builder.add_edge("format_output", END)

graph = builder.compile()
result = graph.invoke({
    "topic": "the benefits of morning exercise",
    "requirements": "target audience: busy professionals. include praticals"
})
print("\n"+"="*10)
print("final result")
print("="*10)
print(result["final_output"])




