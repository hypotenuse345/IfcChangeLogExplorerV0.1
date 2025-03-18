from rdflib import Namespace

CHANGE_LOG = Namespace("http://www.semantic.org/zeyupan/ontologies/change_log_ontology#")
CHANGE_LOG_INST = Namespace("http://www.semantic.org/zeyupan/instances/change_log_ontology#")

def bind_prefixes(g):
    g.bind("clog", CHANGE_LOG)
    g.bind("clogi", CHANGE_LOG_INST)