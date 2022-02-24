from fastapi import FastAPI
from neo4j_connector import Neo4jConnector 
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
neo4j_conn = Neo4jConnector(uri="neo4j+s://e2731293.databases.neo4j.io", user="neo4j", pwd="xxx")

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

    query_string = f"MATCH (n:Lot{year} {{block:\"{block}\"}})-[r:INTERSECTION]->(m) RETURN n,r,m"
    
    edges = []
    for record in neo4j_conn.query(query_string, db='neo4j'):
        left_lot = {"id" : record['r'].nodes[0].id}
        for item in record['r'].nodes[0].items():
            left_lot[item[0]] = item[1]
        
        intersection = {"id" : record['r'].id}
        for item in record['r'].items():
            intersection[item[0]] = item[1]
        
        right_lot = {"id" : record['r'].nodes[1].id}
        for item in record['r'].nodes[1].items():
            right_lot[item[0]] = item[1]
        
        edge = {'left_lot':left_lot, 'intersection': intersection, 'right_lot':right_lot}
        edges.append(edge)
    return edges
