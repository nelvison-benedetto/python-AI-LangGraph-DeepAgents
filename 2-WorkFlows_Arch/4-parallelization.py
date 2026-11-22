
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from typing import TypedDict, Annotated, List

from langchain_openai import ChatOpenAI


class OverallState(TypedDict):
    topic: str
    instagram_post: str
    twitter_post: str
    linkedin_post: str
    final_output: str


llm = ChatOpenAI(model="gpt-4o")

def generate_instagram(state:OverallState)->OverallState:
    print("instagram generator: creting post...")
    prompt=f"""
    create an instagram post about: {state['topic']}
    requirements:
    - engaging and visual language
    - 2-3 short paragraphs (150-200 words max)
    - include relevant emojis
    - end with 5-8 relevant hashtags
    - casual, friendly tone
    - call-to-action to engage with the post
    make it perfect for instagram's audience
    """
    instagram_post= llm.invoke(prompt).content
    print("instagram generator: complete")
    return {
        "instagram_post": instagram_post
    }


def generator_twitter(state:OverallState)->OverallState:
    print("twitter generator: creting post...")
    prompt=f"""
        create an instagram post about: {state['topic']}
        requirements:
        - maximum 280 characters (this is crucial!)
        - punchy and attention-grabbing
        - include 2-3 relevant #
        - conversational tone
        - can use emojis sparingly
        - should spark engagement/replies
        make it perfect for twitter's audience
        """
    twitter_post = llm.invoke(prompt).content
    print("twitter generator: complete")
    return {
            "twitter_post": twitter_post
    }

def aggregate_posts(state:OverallState)->OverallState:
    print("aggregator: combaning all posts...")
    final_output = f"""
    {'='*10}
    social media content package
    {'='*10}
    topic: {state['topic']}
    {'='*10}
    instagram post
    {'='*10}
    {state['instagram_post']}
    {'='*10}
    twitter post
    {'='*10}
    {state['twitter_post']}
    {'='*10}
    """


builder = StateGraph(OverallState)
builder.add_node(generate_instagram)
builder.add_node(generator_twitter)
builder.add_node(aggregate_posts)

builder.add_edge(START, "generate_instagram")
builder.add_edge(START, "generate_twitter")

builder.add_edge("generate_instagram", "aggregate_posts")
builder.add_edge("generate_twitter", "aggregate_posts")

builder.add_edge("aggregate_posts", END)

graph = builder.compile()

topic = "the impact of AI on workplace productivity"

print("\n topic: {topic}:")
result = graph.invoke({
    "topic": topic,
    "instagram_post": "",
    "twitter_post": "",
    "linkedin_post": "",
    "final_output": ""
})

print(result['final_output'])


