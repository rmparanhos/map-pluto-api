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

edge_service = EdgeService()

@app.get("/edges/{year}/{block}")
def get_edges(year: int, block: int):
    return edge_service.get_edges(year, block)

@app.get("/splits/{year}/{initial_block}/{end_block}")
def get_splits(year: int, initial_block: int, end_block: int):
    return edge_service.get_splits(year, initial_block, end_block)

@app.get("/merges/{year}/{initial_block}/{end_block}")
def get_merges(year: int, initial_block: int, end_block: int):
    return edge_service.get_merges(year, initial_block, end_block)

@app.get("/rearranges/{year}/{initial_block}/{end_block}")
def get_rearranges(year: int, initial_block: int, end_block: int):
    return edge_service.get_rearranges(year, initial_block, end_block)
