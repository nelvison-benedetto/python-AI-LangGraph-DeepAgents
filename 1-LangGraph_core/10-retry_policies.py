
from typing import List, Annotated, TypedDict
from langgraph.graph import StateGraph, START, END
from langgraph.graph.messages import add_messages

from langgraph.types import RetryPolicy
import random

class WeatherState(TypedDict):
    city: str
    temperature: float
    condition: str

class APIError(Exception):
    pass

def fetch_weather(state: WeatherState):
    city= state['city']
    if random.random() < 0.7:
        print(f"🔴 - API call failed for {city}")
        raise APIError(f"weather API timeout or {city}")
    print(f"🟢 successfully fetched weather for {city}")
    temp = round(random.uniform(15,30),1)
    conditions = random.choice(["sunny","cloudy","rainy","partially cloudy"])
    return {
        "temperature": temp,
        "conditions": conditions
    }


def format_result(state:WeatherState):
    print(f"\n weather report for {state['city']}")
    print(f"tmperature: {state['temperature']} degrees")
    print(f"conditions: {state['conditions']}")
    return state

builder = StateGraph(WeatherState)

builder.add_node(
    "fetch_weather",
    fetch_weather, 
    retry_policy=RetryPolicy(
        max_attempts=5,
        initial_interval=1,
        backoff_factor=2.0,
        max_interval=10.0,
        jitter=True,
        retry_on=APIError
    )
)
builder.add_node(format_result)
builder.add_edge(START, "fetch_weather")
builder.add_edge("fetch_weather", "format_result")
builder.add_edge("format_result", END)

graph = builder.compile()

## testing

try:
    result=graph.invoke({
        "city": "san francisco",
        "temperature": 0.0,
        "conditions": ""
    })
    print(f"\n final result: {result}")
except Exception as e:
    print(f"\n all retry attempts exhausted: {e}")




