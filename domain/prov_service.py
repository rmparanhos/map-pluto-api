from typing import List
from collections import Counter


class ProvService:

    def __init__(self) -> None:
        pass

    def convert_to_prov_json(self, edges: List[any], merges: List[any], splits: List[any], rearranges: List[any]):
        prov = {}
        prefix = {}
        prefix['xsd'] = "http://www.w3.org/2001/XMLSchema#"
        prefix['prov'] = "http://www.w3.org/ns/prov#"
        prefix['provviz'] = "http://provviz/ns/provviz#"
        prov['prefix'] = prefix
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
        
        splits_intersect_list = []
        splits_left_lot_list = []
        for split in splits:
            prov['activity']["prov:Split" + str(split['left_lot']['id'])] = {}
            splits_left_lot_list.append(split['left_lot']['id'])
            splits_intersect_list.append(split['intersection']['id'])
            
        for edge in edges:
            is_merge = False
            prov['entity']["prov:" + str(edge['left_lot']['YearBBL'])] = {}
            prov['entity']["prov:" + str(edge['right_lot']['YearBBL'])] = {}
            
            if edge['right_lot']['id'] in merges_right_lot_list:   
                wGB = f"_:wGBMerge_{edge['right_lot']['id']}"
                wGBdict = {}
                wGBdict["prov:entity"] = "prov:" + str(edge['right_lot']['YearBBL'])
                wGBdict["prov:activity"] = "prov:Merge" + str(edge['right_lot']['id'])
                prov['wasGeneratedBy'][wGB] = wGBdict
                is_merge = False
            
            if edge['intersection']['id'] in merges_intersect_list:                   
                u = f"_:uMerge_{edge['left_lot']['id']}_{edge['intersection']['id']}"
                udict = {}
                udict["prov:activity"] = "prov:Merge" + str(edge['right_lot']['id'])
                udict["prov:entity"] = "prov:" + str(edge['left_lot']['YearBBL'])
                prov['used'][u] = udict
                is_merge = False
           
            if edge['left_lot']['id'] in splits_left_lot_list:    
                wGB = f"_:wGBSplit_{edge['right_lot']['id']}_{edge['intersection']['id']}"
                wGBdict = {}
                wGBdict["prov:entity"] = "prov:" + str(edge['right_lot']['YearBBL'])
                wGBdict["prov:activity"] = "prov:Split" + str(edge['left_lot']['id'])
                prov['wasGeneratedBy'][wGB] = wGBdict
                if is_merge:
                    wGB = f"_:wGBRearrange_{edge['right_lot']['id']}_{edge['intersection']['id']}"
                    wGBdict = {}
                    wGBdict["prov:entity"] = "prov:" + str(edge['right_lot']['YearBBL'])
                    wGBdict["prov:activity"] = "prov:Rearrange" + str(edge['left_lot']['id'])
                    prov['wasGeneratedBy'][wGB] = wGBdict
                    prov['wasGeneratedBy'].pop(f"_:wGBSplit_{edge['right_lot']['id']}_{edge['intersection']['id']}")
                    prov['wasGeneratedBy'].pop(f"_:wGBMerge_{edge['right_lot']['id']}")     
                
            if edge['intersection']['id'] in splits_intersect_list:   
                u = f"_:uSplit_{edge['left_lot']['id']}"
                udict = {}
                udict["prov:activity"] = "prov:Split" + str(edge['left_lot']['id'])
                udict["prov:entity"] = "prov:" + str(edge['left_lot']['YearBBL'])
                prov['used'][u] = udict
                if is_merge:
                    prov['activity']["prov:Rearrange" + str(edge['left_lot']['id'])] = {}
                    u = f"_:uRearrange_{edge['left_lot']['id']}"
                    udict = {}
                    udict["prov:activity"] = "prov:Rearrange" + str(edge['left_lot']['id'])
                    udict["prov:entity"] = "prov:" + str(edge['left_lot']['YearBBL'])
                    prov['used'][u] = udict
                    prov['used'].pop(f"_:uSplit_{edge['left_lot']['id']}")
                    prov['used'].pop(f"_:uMerge_{edge['left_lot']['id']}_{edge['intersection']['id']}")                 
                
            if edge['intersection']['id'] not in splits_intersect_list and edge['intersection']['id'] not in merges_intersect_list:
                prov['activity']["prov:Maintain" + str(edge['left_lot']['id'])] = {}
                wGB = f"_:wGBMaintain_{edge['left_lot']['id']}"
                wGBdict = {}
                wGBdict["prov:entity"] = "prov:" + str(edge['right_lot']['YearBBL'])
                wGBdict["prov:activity"] = "prov:Maintain" + str(edge['left_lot']['id'])
                prov['wasGeneratedBy'][wGB] = wGBdict
                u = f"_:uMaintain_{edge['left_lot']['id']}"
                udict = {}
                udict["prov:activity"] = "prov:Maintain" + str(edge['left_lot']['id'])
                udict["prov:entity"] = "prov:" + str(edge['left_lot']['YearBBL'])
                prov['used'][u] = udict                 
                #wDF = f"_:wDF{edge['intersection']['id']}"
                #wDFdict = {}
                #wDFdict["prov:usedEntity"] = "prov:" + str(edge['left_lot']['YearBBL'])
                #wDFdict["prov:generatedEntity"] = "prov:" + str(edge['right_lot']['YearBBL'])
                #prov['wasDerivedFrom'][wDF] = wDFdict
        
        return prov
