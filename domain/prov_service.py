from typing import List
from collections import Counter


class ProvService:

    def __init__(self) -> None:
        pass

    def convert_to_prov_json(self, edges: List[any], merges: List[any]):
        prov = {}
        prov['entity'] = {}
        prov['wasDerivedFrom'] = {}
        prov['activity'] = {}
        prov['wasGeneratedBy'] = {}
        prov['used'] = {}
        
        merges_intersect_list = []
        merges_right_lot_list = []
        for merge in merges:
            prov['activity']["prov:Merge" + str(merge['right_lot']['id'])] = {}
            merges_right_lot_list.append(merge['right_lot']['id'])
            merges_intersect_list.append(merge['intersection']['id'])
            
        for edge in edges:
            prov['entity']["prov:" + str(edge['left_lot']['YearBBL'])] = {}
            prov['entity']["prov:" + str(edge['right_lot']['YearBBL'])] = {}
            
            if edge['right_lot']['id'] in merges_right_lot_list:    
                wGB = f"_:wGB{edge['right_lot']['id']}"
                wGBdict = {}
                wGBdict["prov:entity"] = "prov:" + str(edge['right_lot']['YearBBL'])
                wGBdict["prov:activity"] = "prov:Merge" + str(edge['right_lot']['id'])
                prov['wasGeneratedBy'][wGB] = wGBdict
                
            if edge['intersection']['id'] in merges_intersect_list:                   
                u = f"_:u{edge['intersection']['id']}"
                udict = {}
                udict["prov:activity"] = "prov:Merge" + str(edge['right_lot']['id'])
                udict["prov:entity"] = "prov:" + str(edge['left_lot']['YearBBL'])
                prov['used'][u] = udict
                
                continue
            
            wDF = f"_:wDF{edge['intersection']['id']}"
            wDFdict = {}
            wDFdict["prov:usedEntity"] = "prov:" + str(edge['left_lot']['YearBBL'])
            wDFdict["prov:generatedEntity"] = "prov:" + str(edge['right_lot']['YearBBL'])
            prov['wasDerivedFrom'][wDF] = wDFdict
        
        return prov
