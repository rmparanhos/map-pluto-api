from turtle import left
from urllib import response
from fastapi import FastAPI
from neo4j_connector import Neo4jConnector 
from fastapi.middleware.cors import CORSMiddleware
from collections import Counter

app = FastAPI()
neo4j_conn = Neo4jConnector(uri="neo4j://localhost:7687", user="neo4j", pwd="neo4j")

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

@app.get("/edges/{year}/{block}")
def get_edges(year: int, block = int):

    query_string = f"MATCH (n:Lot{year} {{Block:\"{block}\"}})-[r:INTERSECTION]->(m) RETURN n,r,m"
    
    edges = []
    left_edges = []
    right_edges = []
    for record in neo4j_conn.query(query_string, db='neo4j'):
        left_lot = {"id" : record['r'].nodes[0].id}
        left_edges.append(record['r'].nodes[0].id)

        for item in record['r'].nodes[0].items():
            left_lot[item[0]] = item[1]
        
        intersection = {"id" : record['r'].id}
        for item in record['r'].items():
            intersection[item[0]] = item[1]
        
        right_lot = {"id" : record['r'].nodes[1].id}
        right_edges.append(record['r'].nodes[1].id)
        for item in record['r'].nodes[1].items():
            right_lot[item[0]] = item[1]
        
        edge = {'left_lot':left_lot, 'intersection': intersection, 'right_lot':right_lot}
        edges.append(edge)

 
    dict_left_edges = dict(Counter(left_edges))
    dict_right_edges = dict(Counter(right_edges))

    for edge in edges:
        edge['left_lot']['exit_edges'] = dict_left_edges[edge['left_lot']['id']]
        edge['right_lot']['incoming_edges'] = dict_right_edges[edge['right_lot']['id']]
    return edges

@app.get("/splits/{year}/{initial_block}/{end_block}")
def get_splits(year: int, initial_block: int, end_block: int):

    block_list = range(initial_block, end_block)
    query_string = f"MATCH (n:Lot{year})-[r:INTERSECTION]->(m) WHERE n.Block in {[str(block) for block in block_list]} RETURN n,r,m"
    
    edges = []
    left_edges = []
    right_edges = []
    for record in neo4j_conn.query(query_string, db='neo4j'):
        left_lot = {"id" : record['r'].nodes[0].id}
        left_edges.append(record['r'].nodes[0].id)

        for item in record['r'].nodes[0].items():
            left_lot[item[0]] = item[1]
        
        intersection = {"id" : record['r'].id}
        for item in record['r'].items():
            intersection[item[0]] = item[1]
        
        right_lot = {"id" : record['r'].nodes[1].id}
        right_edges.append(record['r'].nodes[1].id)
        for item in record['r'].nodes[1].items():
            right_lot[item[0]] = item[1]
        
        edge = {'left_lot':left_lot, 'intersection': intersection, 'right_lot':right_lot}
        edges.append(edge)

 
    dict_left_edges = dict(Counter(left_edges))
    dict_right_edges = dict(Counter(right_edges))

    response = []
    for edge in edges:
        #splits possuem um numero de arestas de saida maior q dois
        if dict_left_edges[edge['left_lot']['id']] >= 2 :
            edge['left_lot']['exit_edges'] = dict_left_edges[edge['left_lot']['id']]
            edge['right_lot']['incoming_edges'] = dict_right_edges[edge['right_lot']['id']]
            response.append(edge)
    return response


@app.get("/merges/{year}/{initial_block}/{end_block}")
def get_merges(year: int, initial_block: int, end_block: int):

    block_list = range(initial_block, end_block)
    query_string = f"MATCH (n:Lot{year})-[r:INTERSECTION]->(m) WHERE n.Block in {[str(block) for block in block_list]} RETURN n,r,m"
    
    edges = []
    left_edges = []
    right_edges = []
    for record in neo4j_conn.query(query_string, db='neo4j'):
        left_lot = {"id" : record['r'].nodes[0].id}
        left_edges.append(record['r'].nodes[0].id)

        for item in record['r'].nodes[0].items():
            left_lot[item[0]] = item[1]
        
        intersection = {"id" : record['r'].id}
        for item in record['r'].items():
            intersection[item[0]] = item[1]
        
        right_lot = {"id" : record['r'].nodes[1].id}
        right_edges.append(record['r'].nodes[1].id)
        for item in record['r'].nodes[1].items():
            right_lot[item[0]] = item[1]
        
        edge = {'left_lot':left_lot, 'intersection': intersection, 'right_lot':right_lot}
        edges.append(edge)

 
    dict_left_edges = dict(Counter(left_edges))
    dict_right_edges = dict(Counter(right_edges))

    response = []
    for edge in edges:
        #merges possuem um numero de arestas de chegada maior q dois
        if dict_left_edges[edge['rigth_lot']['id']] >= 2 :
            edge['left_lot']['exit_edges'] = dict_left_edges[edge['left_lot']['id']]
            edge['right_lot']['incoming_edges'] = dict_right_edges[edge['right_lot']['id']]
            response.append(edge)
    return response    
