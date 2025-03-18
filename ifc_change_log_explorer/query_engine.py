from pydantic import BaseModel, Field, PrivateAttr
from typing import List, Optional, Union, Any, Dict, Literal

from .item import Item
from chage_log_ontology.namespace import CHANGE_LOG
import rdflib

class ChangeLocation:
    def __init__(self, individual: rdflib.URIRef, rdf_graph: rdflib.Graph):
        self.rdf_graph = rdf_graph
        query_str = """SELECT ?comment WHERE {
            ?individual rdfs:comment ?comment .
        }"""
        comment = self.rdf_graph.query(query_str, initBindings={'individual': individual}).bindings[0]['comment'].toPython()
        self.location = comment


class QueryEngine:
    _create_icon_svg = """<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#308732" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="feather feather-plus-square"><rect x="3" y="3" width="18" height="18" rx="2" ry="2"></rect><line x1="12" y1="8" x2="12" y2="16"></line><line x1="8" y1="12" x2="16" y2="12"></line></svg>"""
    _delete_icon_svg = """<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#D32F2F" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="feather feather-x-square"><rect x="3" y="3" width="18" height="18" rx="2" ry="2"></rect><line x1="9" y1="9" x2="15" y2="15"></line><line x1="15" y1="9" x2="9" y2="15"></line></svg>"""
    _edit_icon_svg = """<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#1976D2" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="feather feather-edit"><path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"></path><path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z"></path></svg>"""
    
    def __init__(self, rdf_graph: rdflib.Graph):
        self.rdf_graph = rdf_graph
        
    def _query_changes(self, mode: Literal["all", "create", "delete", "edit"], entity_keyword: str="") -> List[Item]:
        query_str = """
        SELECT ?entity_label ?link ?type ?description ?location
        WHERE { 
            ?entity a clog:SchematicConcept;
                clog:hasChange ?change;
                rdfs:label ?entity_label.
            OPTIONAL {?entity clog:link ?link.}
            ?change a ?type_class;
                clog:description ?description;
                clog:hasLocation ?location.
            ?type_class clog:data_feather ?type.
        }
        """
        initBindings = None
        if mode.lower() == "create":
            initBindings = {'type_class': CHANGE_LOG.Create}
        elif mode.lower() == "delete":
            initBindings = {'type_class': CHANGE_LOG.Delete}
        elif mode.lower() == "edit":
            initBindings = {'type_class': CHANGE_LOG.Update}
        elif mode.lower() == "all":
            pass
        else:
            raise ValueError(f"Invalid mode: {mode}")
        results = self.rdf_graph.query(query_str, initBindings=initBindings)
        items = []
        for result in results:
            if entity_keyword and entity_keyword.lower() not in result.entity_label.lower():
                continue
            if result.link:
                entity = f"<a href=\"{result.link}\">{result.entity_label}</a>"
            else:
                entity = f"{result.entity_label}"
            if result.type == rdflib.Literal("plus-square"):
                type = self._create_icon_svg
            elif result.type == rdflib.Literal("x-square"):
                type = self._delete_icon_svg
            elif result.type == rdflib.Literal("edit"):
                type = self._edit_icon_svg
            else:
                # raise Exception("Unknown type", result.type)
                type = ""
            location = ChangeLocation(result.location, self.rdf_graph).location
            description = result.description.replace("<a href=\"", "<a href=\"https://ifc43-docs.standards.buildingsmart.org/IFC/RELEASE/IFC4x3/HTML/")
            
            items.append(Item(
                entity=entity, 
                type=type, 
                description=description, 
                location=location,
                entity_label=result.entity_label))
        return items
        
    def query(self, mode:Literal["all", "create", "delete", "edit"], *args, **kwargs) -> List[Item]:
        return self._query_changes(mode, kwargs.get("entity_keyword", ""))
            
        