from typing import Union

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from service import calculate_similarity, calculate_similarity_naive

app = FastAPI()

origins = ["*"]  # Specify allowed origins

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,  # Allow cookies, authorization headers, etc.
    allow_methods=["*"],  # Allow all methods
    allow_headers=["*"],  # Allow all headers
)

# Rest of your API code remains the same

class Documents(BaseModel):
    documentOne: str
    documentTwo: str


@app.get("/")
def read_root():
    return {"Description": "A document similarty checker using Rabin-Karp Algorithm"}


@app.post("/similarity")
def compute_similarity(documents: Documents):
    result = calculate_similarity.calculate_similarity_score(documents.documentOne, documents.documentTwo)
    return {
        "percentage": result["percentage"],
        "classification": result["classification"],
        "breakdown": result["breakdown"]
    }

@app.post("/similarity-naive")
def compute_similarity(documents: Documents):
    result  = calculate_similarity_naive.calculate_similarity_score(documents.documentOne, documents.documentTwo)
    return {
        "percentage": result["percentage"],
        "classification": result["classification"],
        "breakdown": result["breakdown"]
    }