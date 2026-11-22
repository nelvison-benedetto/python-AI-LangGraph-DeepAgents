
from typing import List, Annotated, TypedDict
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages

from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field
import json


class ProductReview(BaseModel):
    product_name: str = Field(description="name of the product")
    sentiment: str = Field(description="overall sentiment: positive, negative or neutral")
    rating: int = Field(description="rating from 1-5", ge=1, le=5 )
    pros: List[str] = Field(description="list of positive aspects")
    cons: List[str] = Field(description="list of negative aspects")
    summary: str = Field(description="brief summary of the review")

llm = ChatOpenAI(model="gtp-4o")
structured_llm = llm.with_structured_output(ProductReview)
prompt = ChatPromptTemplate.from_messages([
    ("system", "you are a product review analyzer. Extract structured info from reviews"), 
    ("user", "{review_text}")
])

chain = prompt | structured_llm

review_text = """"i bought this wireless mouse last month and it's been mostly great. however, the scroll wheel is a bit stiff and makes clicking sounds. also, it's quite expensive compared to similar models. overall, i'd give it 4 out of 5 stars."""

result = chain.invoke({
    "review_text": review_text
})

print(json.dumps(result.model_dump(), indent=2 ))




