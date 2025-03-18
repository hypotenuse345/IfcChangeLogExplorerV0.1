# %%
import os
import json

with open("./outputs/change_log_jsons/ifc4.3.2_change_log.json", "r") as f:
    data = json.load(f)

locations = set()

for item_name, item_data in data.items():
    for change in item_data["changes"]:
        locations.add(change["location"])
# %%
print(len(locations))
# %%
from pyparsing import *
where_rule_pattern = CaselessLiteral("WHERE") + CaselessLiteral("RULE") + Optional(Word(alphanums + "-_")("rule_name")) + Optional(Word(alphanums + "-_")("rule_change"))
unique_rule_pattern = CaselessLiteral("UNIQUE") + CaselessLiteral("RULE")
property_pattern = CaselessLiteral("PROPERTY") + Optional(Word(alphanums + "-_")("property_name"))
super_pattern = CaselessLiteral("SUPERTYPE")
item_pattern = CaselessLiteral("ITEM") + Optional(Word(alphanums + "-_")("item_name"))
inverse_attribute_pattern = CaselessLiteral("INVERSE") + CaselessLiteral("ATTRIBUTE") + Optional(Word(alphanums + "-_")("attribute_name")) + Optional(Word(alphanums + "-_")("attribute_change"))
direct_attribute_pattern = CaselessLiteral("ATTRIBUTE") + Optional(Word(alphanums + "-_")("attribute_name")) + Optional(Word(alphanums + "-_")("attribute_change"))
deprecated_pattern = CaselessLiteral("DEPRECATED")
abstract_pattern = CaselessLiteral("ABSTRACT")
type_pattern = CaselessLiteral("TYPE")
applicability_pattern = CaselessLiteral("APPLICABILITY")
location_pattern = where_rule_pattern("where_rule") | unique_rule_pattern("unique_rule") | property_pattern("property") | super_pattern("supertype") | item_pattern("item") | inverse_attribute_pattern("inverse_attribute") | direct_attribute_pattern("direct_attribute") | deprecated_pattern("deprecated") | abstract_pattern("abstract") | applicability_pattern("applicability") | type_pattern("type")

# %%
results = []

for location in locations:
    if location.strip() == "":
        results.append({})
        continue
    try:
        result = location_pattern.parseString(location)
        result = result.asDict()
        to_out = {}
        if result.get("where_rule"):
            to_out["type"] = "where_rule"
            to_out["rule_name"] = result.get("rule_name", "")
            to_out["rule_change"] = result.get("rule_change", "")
        elif result.get("property"):
            to_out["type"] = "property"
            to_out["property_name"] = result.get("property_name", "")
        elif result.get("supertype"):
            to_out["type"] = "supertype"
        elif result.get("item"):
            to_out["type"] = "item"
            to_out["item_name"] = result.get("item_name", "")
        elif result.get("inverse_attribute"):
            to_out["type"] = "inverse_attribute"
            to_out["attribute_name"] = result.get("attribute_name", "")
            to_out["attribute_change"] = result.get("attribute_change", "")
        elif result.get("direct_attribute"):
            to_out["type"] = "direct_attribute"
            to_out["attribute_name"] = result.get("attribute_name", "")
            to_out["attribute_change"] = result.get("attribute_change", "")
        elif result.get("deprecated"):
            to_out["type"] = "deprecated"
        elif result.get("abstract"):
            to_out["type"] = "abstract"
        elif result.get("applicability"):
            to_out["type"] = "applicability"
        elif result.get("type"):
            to_out["type"] = "type"
        elif result.get("unique_rule"):
            to_out["type"] = "unique_rule"
        else:
            raise ParseException("Unknown type")
        to_out["location"] = location
        results.append(to_out)
    except ParseException as e:
        print(location)
        print(e)
    
# %%
import pprint as pp
pp.pprint(locations)
# %%
