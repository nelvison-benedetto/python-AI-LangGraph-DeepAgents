
from typing import List, TypedDict, Annotated
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages

from langchain_openai import ChatOpenAI
from langchain_core.tools import tool


@tool
def get_weather(city: str)->str:
    weather_data = {
        "new york": "sunny 72f",
        "london": "cloudy 15f",
        "tokyo": "rainy 20c"
    }
    return weather_data.get(city, "weather data not available")

@tool
def calculate_tip(bill_amount: float, tip_percentage: float)->float:
    return round(bill_amount*(tip_percentage/100), 2)

llm = ChatOpenAI(
    model="gpt-4o"
)

llm_with_tools = llm.bind_tools({get_weather, calculate_tip})

weather_prompts = "what's the weather in tokyo"
tip_prompt = "calculate a 20%"





