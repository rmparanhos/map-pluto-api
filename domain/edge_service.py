from typing import List
from collections import Counter

from infrastructure.edge_repository import EdgeRepository
from infrastructure.data.filter import Filter

class EdgeService:

    def __init__(self) -> None:
        self.edge_repository = EdgeRepository()
        pass

    def get_edges(self, year: int, initial_block: int, end_block: int, filter_list: List[Filter]):
    
        edges = []
        left_edges = []
        right_edges = []
        for record in self.edge_repository.get_edges_by_blocklist(year, initial_block, end_block, filter_list):
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

    def get_splits(self, year: int, initial_block: int, end_block: int, filter_list: List[Filter]):

        edges = []
        left_edges = []
        right_edges = []
        for record in self.edge_repository.get_edges_by_blocklist(year, initial_block, end_block, filter_list):
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

    def get_merges(self, year: int, initial_block: int, end_block: int, filter_list: List[Filter]):
       
        edges = []
        left_edges = []
        right_edges = []
        for record in self.edge_repository.get_edges_by_blocklist(year, initial_block, end_block, filter_list):
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

    def get_rearranges(self, year: int, initial_block: int, end_block: int, filter_list: List[Filter]):
         
        edges = []
        left_edges = []
        right_edges = []
        #TODO FILTRO QUEBRADO NO REARRENGE, POIS O FILTRO FAZ COM QUE ELE NAO SE ENCAIXE MAIS NO CRITERIO DE REARRANGE
        for record in self.edge_repository.get_edges_by_blocklist(year, initial_block, end_block, filter_list):
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
            #TODO 
            #FILTRO QUEBRADO NO REARRENGE, POIS O FILTRO FAZ COM QUE ELE NAO SE ENCAIXE MAIS NO CRITERIO DE REARRANGE
            #E AI NAO ENTRA NESSE IF, EXEMPLO WHERE n.Block in [16] AND (n.LotArea >= 3200.0 OR m.LotArea >= 3200.0) AND (n.Address = 'JOE DIMAGGIO HIGHWAY' OR m.Address = 'JOE DIMAGGIO HIGHWAY')
            if dict_right_edges[edge['right_lot']['id']] >= 2 and dict_left_edges[edge['left_lot']['id']] >= 2:
                edge['left_lot']['exit_edges'] = dict_left_edges[edge['left_lot']['id']]
                edge['right_lot']['incoming_edges'] = dict_right_edges[edge['right_lot']['id']]
                rearrange_edges = self.insert_edge_ordered(rearrange_edges, edge)
                rearrange_bbl.append(edge['left_lot']['YearBBL'])
                rearrange_bbl.append(edge['right_lot']['YearBBL'])

        #voltando nos splits e merges para capturar toda a participacao do rearranjo
        splits = self.get_splits(year, initial_block, end_block, [])
        for edge in splits:
            if (edge['left_lot']['YearBBL'] in rearrange_bbl or edge['right_lot']['YearBBL'] in rearrange_bbl):
                rearrange_edges = self.insert_edge_ordered(rearrange_edges, edge)
                rearrange_bbl.append(edge['left_lot']['YearBBL'])
                rearrange_bbl.append(edge['right_lot']['YearBBL'])

        merges = self.get_merges(year, initial_block, end_block, [])
        for edge in merges:
            if (edge['left_lot']['YearBBL'] in rearrange_bbl or edge['right_lot']['YearBBL'] in rearrange_bbl):
                rearrange_edges = self.insert_edge_ordered(rearrange_edges, edge)
                rearrange_bbl.append(edge['left_lot']['YearBBL'])
                rearrange_bbl.append(edge['right_lot']['YearBBL'])
        return rearrange_edges

    def insert_edge_ordered(self, edges_list, edge_to_insert):
        resp = []
        if len(edges_list) == 0: return [edge_to_insert]
        inserted = False
        for edge in edges_list:
            if(edge_to_insert['left_lot']['Block'] < edge['left_lot']['Block']):
                resp.append(edge_to_insert)
                inserted = True
            resp.append(edge)    
        if not inserted:
            resp.append(edge_to_insert)
        return resp