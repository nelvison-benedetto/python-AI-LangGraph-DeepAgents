
from typing import List, Annotated, TypedDict
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages

from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field
import json


class ProductReview(BaseModel):
    product_name: str = Field(description="name of the product")
    sentiment: str = Field(description=overall sentiment: positive, negative, or neutral)
    rating: int = Field(description="rating from 1-5", ge=1 le=5)
    pros: List[str] = Field(description="list of positive aspects")
    cons: List[str] = Field(description="list of negative aspects")
    summary: 



