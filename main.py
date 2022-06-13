from typing import List
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def hello_world():
    return {"Hello": "World"}

from domain.edge_service import EdgeService
from infrastructure.data.filter import Filter

edge_service = EdgeService()

@app.post("/edges/{year}/{initial_block}/{end_block}")
def get_edges(year: int, initial_block: int, end_block: int, filter_list: List[Filter]):
    return edge_service.get_edges(year, initial_block, end_block, filter_list)

@app.get("/splits/{year}/{initial_block}/{end_block}")
def get_splits(year: int, initial_block: int, end_block: int):
    return edge_service.get_splits(year, initial_block, end_block)

@app.get("/merges/{year}/{initial_block}/{end_block}")
def get_merges(year: int, initial_block: int, end_block: int):
    return edge_service.get_merges(year, initial_block, end_block)

@app.get("/rearranges/{year}/{initial_block}/{end_block}")
def get_rearranges(year: int, initial_block: int, end_block: int):
    return edge_service.get_rearranges(year, initial_block, end_block)
