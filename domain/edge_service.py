from infrastructure.neo4j_repository import Neo4jRepository 
from collections import Counter

class EdgeService:

    def __init__(self) -> None:
        self.neo4j_conn = Neo4jRepository(uri="neo4j://localhost:7687", user="neo4j", pwd="neo4j")
        pass

    def get_edges(self, year: int, block: int):
        query_string = f"MATCH (n:Lot{year} {{Block:\"{block}\"}})-[r:INTERSECTION]->(m) RETURN n,r,m"
    
        edges = []
        left_edges = []
        right_edges = []
        for record in self.neo4j_conn.query(query_string, db='neo4j'):
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

    def get_splits(self, year: int, initial_block: int, end_block: int):
        block_list = range(initial_block, end_block+1)
        query_string = f"MATCH (n:Lot{year})-[r:INTERSECTION]->(m) WHERE n.Block in {[str(block) for block in block_list]} RETURN n,r,m"
        
        edges = []
        left_edges = []
        right_edges = []
        for record in self.neo4j_conn.query(query_string, db='neo4j'):
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
            if dict_left_edges[edge['left_lot']['id']] >= 2 and dict_right_edges[edge['right_lot']['id']] == 1:
                edge['left_lot']['exit_edges'] = dict_left_edges[edge['left_lot']['id']]
                edge['right_lot']['incoming_edges'] = dict_right_edges[edge['right_lot']['id']]
                response.append(edge)
        return response

    def get_merges(self, year: int, initial_block: int, end_block: int):
        block_list = range(initial_block, end_block+1)
        query_string = f"MATCH (n:Lot{year})-[r:INTERSECTION]->(m) WHERE n.Block in {[str(block) for block in block_list]} RETURN n,r,m"

        edges = []
        left_edges = []
        right_edges = []
        for record in self.neo4j_conn.query(query_string, db='neo4j'):
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
            if dict_left_edges[edge['left_lot']['id']] == 1 and dict_right_edges[edge['right_lot']['id']] >= 2:
                edge['left_lot']['exit_edges'] = dict_left_edges[edge['left_lot']['id']]
                edge['right_lot']['incoming_edges'] = dict_right_edges[edge['right_lot']['id']]
                response.append(edge)
        return response 

    def get_rearranges(self, year: int, initial_block: int, end_block: int):
        block_list = range(initial_block, end_block+1)
        query_string = f"MATCH (n:Lot{year})-[r:INTERSECTION]->(m) WHERE n.Block in {[str(block) for block in block_list]} RETURN n,r,m"
        
        edges = []
        left_edges = []
        right_edges = []
        for record in self.neo4j_conn.query(query_string, db='neo4j'):
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

        rearrange_edges = []
        rearrange_bbl = []
        for edge in edges:
            #nxm possuem um numero de arestas de chegada e saida maior q dois
            if dict_right_edges[edge['right_lot']['id']] >= 2 and dict_left_edges[edge['left_lot']['id']] >= 2:
                edge['left_lot']['exit_edges'] = dict_left_edges[edge['left_lot']['id']]
                edge['right_lot']['incoming_edges'] = dict_right_edges[edge['right_lot']['id']]
                rearrange_edges.append(edge)
                rearrange_bbl.append(edge['left_lot']['YearBBL'])
                rearrange_bbl.append(edge['right_lot']['YearBBL'])
        print(rearrange_bbl)
        for item in rearrange_edges:
            print(item['left_lot']['YearBBL'])
            print(item['intersection']['area'])
            print(item['right_lot']['YearBBL'])

        #voltando nos splits e merges para capturar toda a participacao do rearranjo
        splits = self.get_splits(year, initial_block, end_block)
        for edge in splits:
            if (edge['left_lot']['YearBBL'] in rearrange_bbl or edge['right_lot']['YearBBL'] in rearrange_bbl):
                rearrange_edges.append(edge)
                rearrange_bbl.append(edge['left_lot']['YearBBL'])
                rearrange_bbl.append(edge['right_lot']['YearBBL'])
        print(rearrange_bbl)
        for item in rearrange_edges:
            print(item['left_lot']['YearBBL'])
            print(item['intersection']['area'])
            print(item['right_lot']['YearBBL'])

        merges = self.get_merges(year, initial_block, end_block)
        for edge in merges:
            if (edge['left_lot']['YearBBL'] in rearrange_bbl or edge['right_lot']['YearBBL'] in rearrange_bbl):
                rearrange_edges.append(edge)
                rearrange_bbl.append(edge['left_lot']['YearBBL'])
                rearrange_bbl.append(edge['right_lot']['YearBBL'])
        print(rearrange_bbl)
        for item in rearrange_edges:
            print(item['left_lot']['YearBBL'])
            print(item['intersection']['area'])
            print(item['right_lot']['YearBBL'])

        return rearrange_edges  