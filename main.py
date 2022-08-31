from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import datetime

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

from typing import List
from domain.edge_service import EdgeService
from infrastructure.data.filter import Filter

edge_service = EdgeService()

@app.get("/")
def hello_world():
    return {"Hello": "World"}

@app.post("/edges/{initial_year}/{end_year}/{initial_block}/{end_block}")
def get_edges(initial_year: int, end_year: int, initial_block: int, end_block: int, filter_list: List[Filter]):
    if initial_year == end_year or initial_year+1 == end_year: return edge_service.get_edges_by_blocklist(initial_year, initial_block, end_block, filter_list)
    
    resp = []
    for year in range(initial_year, end_year):
        resp = resp + edge_service.get_edges_by_blocklist(year, initial_block, end_block, filter_list)
    return resp

@app.post("/splits/{initial_year}/{end_year}/{initial_block}/{end_block}")
def get_splits(initial_year: int, end_year: int, initial_block: int, end_block: int, filter_list: List[Filter]):
    if initial_year == end_year or initial_year+1 == end_year: return edge_service.get_splits(initial_year, initial_block, end_block, filter_list)
    
    resp = []
    for year in range(initial_year, end_year):
        t = datetime.datetime.now()
        resp = resp + edge_service.get_splits(year, initial_block, end_block, filter_list)
        print(datetime.datetime.now()-t)
    
    bbls = []
    for edge in resp:     
        if edge['left_lot']['BBL'] not in bbls: bbls.append(edge['left_lot']['BBL'])
        if edge['right_lot']['BBL'] not in bbls: bbls.append(edge['right_lot']['BBL'])

    return edge_service.get_edges_by_bbl(bbls,initial_year,end_year)

@app.post("/merges/{initial_year}/{end_year}/{initial_block}/{end_block}")
def get_merges(initial_year: int, end_year: int, initial_block: int, end_block: int, filter_list: List[Filter]):
    if initial_year == end_year or initial_year+1 == end_year: return edge_service.get_merges(initial_year, initial_block, end_block, filter_list)
    
    resp = []
    for year in range(initial_year, end_year):
        resp = resp + edge_service.get_merges(year, initial_block, end_block, filter_list)
    
    bbls = []
    for edge in resp:     
        if edge['left_lot']['BBL'] not in bbls: bbls.append(edge['left_lot']['BBL'])
        if edge['right_lot']['BBL'] not in bbls: bbls.append(edge['right_lot']['BBL'])

    return edge_service.get_edges_by_bbl(bbls,initial_year,end_year)


@app.post("/get_rearrange/{initial_year}/{end_year}/{initial_block}/{end_block}")
def get_rearranges(initial_year: int, end_year: int, initial_block: int, end_block: int, filter_list: List[Filter]):
    if initial_year == end_year or initial_year+1 == end_year: return edge_service.get_rearranges(initial_year, initial_block, end_block, filter_list)
    
    resp = []
    for year in range(initial_year, end_year):
        resp = resp + edge_service.get_rearranges(year, initial_block, end_block, filter_list)

    bbls = []
    for edge in resp:     
        if edge['left_lot']['BBL'] not in bbls: bbls.append(edge['left_lot']['BBL'])
        if edge['right_lot']['BBL'] not in bbls: bbls.append(edge['right_lot']['BBL'])

    return edge_service.get_edges_by_bbl(bbls,initial_year,end_year)
