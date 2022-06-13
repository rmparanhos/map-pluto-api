from typing import List
from config.neo4j_helper import Neo4jHelper
from infrastructure.data.filter import Filter

class EdgeRepository:
    
    def __init__(self) -> None:
        self.neo4j_conn = Neo4jHelper(uri="neo4j://localhost:7687", user="neo4j", pwd="neo4j")
        pass

    def get_edges_by_block(self, year: int, block: int):
        query_string = f"MATCH (n:Lot{year} {{Block:\"{block}\"}})-[r:INTERSECTION]->(m) RETURN n,r,m"
    
        return self.neo4j_conn.query(query_string, db='neo4j')
    
    def get_edges_by_blocklist(self, year: int, initial_block: int, end_block: int, filter_list: List[Filter]):
        block_list = range(initial_block, end_block+1)
        query_string = f"MATCH (n:Lot{year})-[r:INTERSECTION]->(m) WHERE n.Block in {[str(block) for block in block_list]}"
        for filter in filter_list:
            query_string += f" AND n.{filter.attribute} {filter.operand} '{filter.value}'"
        query_string += " RETURN n,r,m"
        print(query_string)
        return self.neo4j_conn.query(query_string, db='neo4j')

