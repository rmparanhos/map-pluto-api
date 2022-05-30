#nao funciona ainda esse controller
from main import app
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
   

""" @app.get("/rearrange/{year}/{initial_block}/{end_block}")
def get_rearrange(year: int, initial_block: int, end_block: int):

    block_list = range(initial_block, end_block+1)
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
        #nxm possuem um numero de arestas de chegada e saida maior q dois
        print('----')
        print(dict_right_edges[edge['right_lot']['id']])
        print(dict_left_edges[edge['left_lot']['id']])
        if dict_right_edges[edge['right_lot']['id']] >= 2 and dict_left_edges[edge['left_lot']['id']] >= 2:
            edge['left_lot']['exit_edges'] = dict_left_edges[edge['left_lot']['id']]
            edge['right_lot']['incoming_edges'] = dict_right_edges[edge['right_lot']['id']]
            response.append(edge)
    return response   """