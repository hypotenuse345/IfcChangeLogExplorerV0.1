from datetime import datetime
from rdflib import Literal, BNode, URIRef, DCTERMS, SDO, RDFS, RDF, OWL
from rdflib.collection import Collection

from .namespace import CHANGE_LOG, bind_prefixes

# 元数据
ontology_metadata = {
    DCTERMS.creator: [
        {
            RDF.type: SDO.Person,
            SDO.email: Literal("panzeyu@sjtu.edu.cn"),
            SDO.name: Literal('Pan Zeyu')
        }
    ],
    DCTERMS.issued: Literal("2025-03-17"),
    DCTERMS.modified: Literal(datetime.now().strftime("%Y-%m-%d")),
    RDFS.label: Literal("Change Log Ontology"),
}

def define_ontology(g):
    ontology_metadata_copy = ontology_metadata.copy()
    ontology = URIRef("http://www.semantic.org/zeyupan/ontologies/change_log_ontology")
    g.add((ontology, RDF.type, OWL.Ontology))
    
    creators = []
    creator_list = BNode()
    for creator in ontology_metadata_copy.pop(DCTERMS.creator):
        creator1 = BNode()
        creators.append(creator1)
        for k, v in creator.items():
            g.add((creator1, k, v))
    
    Collection(g,creator_list,creators)
    g.add((ontology, DCTERMS.creator, creator_list))
    
    for k, v in ontology_metadata_copy.items():
        g.add((ontology, k, v))