from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import datetime
import time

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
from domain.prov_service import ProvService
from infrastructure.data.filter import Filter

edge_service = EdgeService()
prov_service = ProvService()

@app.get("/")
def hello_world():
    return {"Hello": "World"}

@app.post("/edges/{initial_year}/{end_year}/{initial_block}/{end_block}")
def get_edges(initial_year: int, end_year: int, initial_block: int, end_block: int, borough: str, filter_list: List[Filter]):
    if initial_year == end_year or initial_year+1 == end_year: return edge_service.get_edges_by_blocklist(initial_year, initial_block, end_block, borough, filter_list)
    
    resp = []
    for year in range(initial_year, end_year):
        resp = resp + edge_service.get_edges_by_blocklist(year, initial_block, end_block, borough, filter_list)
    return resp

@app.post("/splits/{initial_year}/{end_year}/{initial_block}/{end_block}")
def get_splits(initial_year: int, end_year: int, initial_block: int, end_block: int, borough: str, filter_list: List[Filter]):
    if initial_year == end_year or initial_year+1 == end_year: return edge_service.get_splits(initial_year, initial_block, end_block, borough, filter_list)
    
    resp = []
    for year in range(initial_year, end_year):
        t = datetime.datetime.now()
        resp = resp + edge_service.get_splits(year, initial_block, end_block, borough, filter_list)
        print(datetime.datetime.now()-t)
    
    bbls = []
    for edge in resp:     
        if edge['left_lot']['BBL'] not in bbls: bbls.append(edge['left_lot']['BBL'])
        if edge['right_lot']['BBL'] not in bbls: bbls.append(edge['right_lot']['BBL'])

    return edge_service.get_edges_by_bbl(bbls,initial_year,end_year)

@app.post("/merges/{initial_year}/{end_year}/{initial_block}/{end_block}/{borough}")
def get_merges(initial_year: int, end_year: int, initial_block: int, end_block: int, borough: str, filter_list: List[Filter]):
    if initial_year == end_year or initial_year+1 == end_year: return edge_service.get_merges(initial_year, initial_block, end_block, borough, filter_list)
    
    resp = []
    for year in range(initial_year, end_year):
        resp = resp + edge_service.get_merges(year, initial_block, end_block, borough, filter_list)
    
    bbls = []
    for edge in resp:     
        if edge['left_lot']['BBL'] not in bbls: bbls.append(edge['left_lot']['BBL'])
        if edge['right_lot']['BBL'] not in bbls: bbls.append(edge['right_lot']['BBL'])
    #return resp
    return edge_service.get_edges_by_bbl(bbls,initial_year,end_year)


@app.post("/rearranges/{initial_year}/{end_year}/{initial_block}/{end_block}/{borough}")
def get_rearranges(initial_year: int, end_year: int, initial_block: int, end_block: int, borough: str, filter_list: List[Filter]):
    if initial_year == end_year or initial_year+1 == end_year: return edge_service.get_rearranges(initial_year, initial_block, end_block, borough, filter_list)
    
    resp = []
    for year in range(initial_year, end_year):
        resp = resp + edge_service.get_rearranges(year, initial_block, end_block, borough, filter_list)

    bbls = []
    for edge in resp:     
        if edge['left_lot']['BBL'] not in bbls: bbls.append(edge['left_lot']['BBL'])
        if edge['right_lot']['BBL'] not in bbls: bbls.append(edge['right_lot']['BBL'])

    return edge_service.get_edges_by_bbl(bbls,initial_year,end_year)


@app.post("/edges_as_prov/{initial_year}/{end_year}/{initial_block}/{end_block}/{borough}/{with_attributes}/{with_rearranges}")
def get_edges_as_prov(initial_year: int, end_year: int, initial_block: int, end_block: int, borough: str, with_attributes: bool, with_rearranges: bool, filter_list: List[Filter]):
    if initial_year == end_year: end_year += 1
    
    tic_master = time.perf_counter()
    
    tic_edges = time.perf_counter()
    resp = []
    for year in range(initial_year, end_year):
        resp = resp + edge_service.get_edges_by_blocklist(year, initial_block, end_block, borough, filter_list)
    print(f"Took {time.perf_counter()- tic_edges:0.4f} seconds edges")
    
    tic_merges = time.perf_counter()    
    merges = []
    for year in range(initial_year, end_year):
        merges = merges + edge_service.get_merges(year, initial_block, end_block, borough, filter_list)
    print(f"Took {time.perf_counter()- tic_merges:0.4f} seconds merges")
    
    tic_splits = time.perf_counter()
    splits = []
    for year in range(initial_year, end_year):
        splits = splits + edge_service.get_splits(year, initial_block, end_block, borough, filter_list)
    print(f"Took {time.perf_counter()- tic_splits:0.4f} seconds splits")
    
    tic_rearrange = time.perf_counter()
    rearranges_ids = {}
    for year in range(initial_year, end_year):
        rearranges_ids[str(year)+str(year+1)] = edge_service.get_rearranges_ids(year, initial_block, end_block, borough, filter_list)
    print(f"Took {time.perf_counter()- tic_rearrange:0.4f} seconds rearrange")
    
    tic_conversion = time.perf_counter()
    x = prov_service.convert_to_prov_json(resp,merges,splits,rearranges_ids,with_attributes=with_attributes,with_rearranges=with_rearranges)
    print(f"Took {time.perf_counter()- tic_conversion:0.4f} seconds conversion")
    
    print(f"Took {time.perf_counter()- tic_master:0.4f} seconds")
   
    return x