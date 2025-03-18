# %%
from rdflib import RDF, URIRef, Literal, Graph, Namespace, BNode, RDFS
import os
from tqdm.notebook import tqdm
import json

from chage_log_ontology.namespace import CHANGE_LOG, CHANGE_LOG_INST, bind_prefixes

def parse_change_location(G:Graph, location_node, detailed_location):
    if detailed_location.get("type", None) is None:
        G.add((location_node, RDF.type, CHANGE_LOG.UndefinedChangeLoc))
        return
    loc_type = detailed_location["type"]
    if loc_type.lower() == "abstract":
        G.add((location_node, RDF.type, CHANGE_LOG.AbstractChangeLoc))
    elif loc_type.lower() == "applicability":
        G.add((location_node, RDF.type, CHANGE_LOG.ApplicabilityChangeLoc))
    elif loc_type.lower() == "deprecated":
        G.add((location_node, RDF.type, CHANGE_LOG.DeprecatedChangeLoc))
    elif loc_type.lower() == "supertype":
        G.add((location_node, RDF.type, CHANGE_LOG.SupertypeChangeLoc))
    elif loc_type.lower() == "type":
        G.add((location_node, RDF.type, CHANGE_LOG.TypeChangeLoc))
    elif loc_type.lower() == "direct_attribute":
        G.add((location_node, RDF.type, CHANGE_LOG.DirectAttributeChangeLoc))
        if detailed_location.get("attribute_name",""):
            G.add((location_node, RDFS.label, Literal(detailed_location["attribute_name"])))
        if detailed_location.get("attribute_change",""):
            G.add((location_node, CHANGE_LOG.changed, Literal(detailed_location["attribute_change"])))
    elif loc_type.lower() == "inverse_attribute":
        G.add((location_node, RDF.type, CHANGE_LOG.InverseAttributeChangeLoc))
        if detailed_location.get("attribute_name",""):
            G.add((location_node, RDFS.label, Literal(detailed_location["attribute_name"])))
        if detailed_location.get("attribute_change",""):
            G.add((location_node, CHANGE_LOG.changed, Literal(detailed_location["attribute_change"])))
    elif loc_type.lower() == "item":
        G.add((location_node, RDF.type, CHANGE_LOG.ItemChangeLoc))
        if detailed_location.get("item_name",""):
            G.add((location_node, RDFS.label, Literal(detailed_location["item_name"])))
    elif loc_type.lower() == "property":
        G.add((location_node, RDF.type, CHANGE_LOG.PropertyChangeLoc))
        if detailed_location.get("property_name",""):
            G.add((location_node, RDFS.label, Literal(detailed_location["property_name"])))
        if detailed_location.get("property_change",""):
            G.add((location_node, CHANGE_LOG.changed, Literal(detailed_location["property_change"])))
    elif loc_type.lower() == "where_rule":
        G.add((location_node, RDF.type, CHANGE_LOG.WhereRuleChangeLoc))
        if detailed_location.get("rule_name",""):
            G.add((location_node, RDFS.label, Literal(detailed_location["rule_name"])))
        if detailed_location.get("rule_change",""):
            G.add((location_node, CHANGE_LOG.changed, Literal(detailed_location["rule_change"])))
    elif loc_type.lower() == "unique_rule":
        G.add((location_node, RDF.type, CHANGE_LOG.UniqueRuleChangeLoc))
        if detailed_location.get("rule_name",""):
            G.add((location_node, RDFS.label, Literal(detailed_location["rule_name"])))
        if detailed_location.get("rule_change",""):
            G.add((location_node, CHANGE_LOG.changed, Literal(detailed_location["rule_change"])))
    else:
        print(f"Unknown location type: {loc_type}")

def instantiation(filepath, G: Graph):
    with open(filepath, "r") as f:
        data = json.load(f)
    filename = os.path.splitext(os.path.basename(filepath))[0]
    print(f"Processing {filename}")
    for concept_name, concept_data in tqdm(data.items()):
        concept = CHANGE_LOG_INST[concept_name]
        G.add((concept, RDF.type, CHANGE_LOG.SchematicConcept))
        G.add((concept, RDFS.label, Literal(concept_name)))
        if concept_data["link"]:
            G.add((concept, CHANGE_LOG.link, Literal(f'https://ifc43-docs.standards.buildingsmart.org/IFC/RELEASE/IFC4x3/HTML/{concept_data["link"]}')))
        for ii, change in enumerate(concept_data["changes"]):
            if change["type"] == "x-square":
                change_node = CHANGE_LOG_INST[f"Delete_{concept_name}_{ii+1}"]
                G.add((change_node, RDF.type, CHANGE_LOG.Delete))
            elif change["type"] == "plus-square":
                change_node = CHANGE_LOG_INST[f"Create_{concept_name}_{ii+1}"]
                G.add((change_node, RDF.type, CHANGE_LOG.Create))
            elif change["type"] == "edit":
                change_node = CHANGE_LOG_INST[f"Update_{concept_name}_{ii+1}"]
                G.add((change_node, RDF.type, CHANGE_LOG.Update))
            else:
                raise ValueError(f"Unknown change type: {change['type']}")
            G.add((concept, CHANGE_LOG.hasChange, change_node))
            location = CHANGE_LOG_INST[f"Location_{concept_name}_{ii+1}"]
            G.add((change_node, CHANGE_LOG.hasLocation, location))
            G.add((location, RDFS.comment, Literal(change["location"])))
            detailed_location = change["location_detailed"]
            parse_change_location(G, location, detailed_location)
            
            # G.add((change_node, CHANGE_LOG.location, Literal(change["location"])))
            G.add((change_node, CHANGE_LOG.description, Literal(change["description"])))
            
    output_dir = "./outputs/change_log_ttls"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    G.serialize(destination=os.path.join(output_dir, f"{filename}.ttl"), format="turtle")

# %%
source_dir = "./outputs/change_log_jsons/"
for filename in os.listdir(source_dir):
    G = Graph()
    bind_prefixes(G)
    G.parse("./change_log_ontology.ttl", format="turtle")

    filepath = os.path.join(source_dir, filename)
    if os.path.isfile(filepath):
        instantiation(filepath, G)
# %%
