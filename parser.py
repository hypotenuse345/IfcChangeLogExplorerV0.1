# %%
from pyparsing import *

def get_td_pattern():
    # 定义HTML标签的解析规则
    tag = Word(alphas)
    attribute = Word(alphanums + "-_") + "=" + quotedString
    openTag = Literal("<") + tag("tag_name") + Optional(ZeroOrMore(attribute)) + Literal(">")
    closeTag = Literal("</") + tag + Literal(">")

    # 当前需求相关的HTML标签解析规则
    data_label = CaselessKeyword('data-label') + '=' + quotedString("label")
    td_open = Literal('<td') + data_label + Literal('>')
    td_close = Literal('</td>')
    # 解析内容
    content = SkipTo(td_close)

    # 构建整个<tr>行的解析模式
    row_pattern = openTag.suppress() + td_open + content("type") + td_close.suppress() + \
        td_open + content("entity") + td_close.suppress() + \
        td_open + content("location") + td_close.suppress() + \
        td_open + content("description") + td_close.suppress() + \
        closeTag.suppress()
    return row_pattern

def get_location_pattern():
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

    location_pattern = (
        where_rule_pattern("where_rule") | unique_rule_pattern("unique_rule") | 
        property_pattern("property") | super_pattern("supertype") | 
        item_pattern("item") | inverse_attribute_pattern("inverse_attribute") | 
        direct_attribute_pattern("direct_attribute") | deprecated_pattern("deprecated") | 
        abstract_pattern("abstract") | applicability_pattern("applicability") | type_pattern("type"))
    return location_pattern

entity_with_link = Literal("<a") + Literal("href") +Literal("=")+quotedString("link") + Literal(">") + SkipTo(Literal("</a>"))("entity_name") + Literal("</a>")
type_pattern = Literal("<i data-feather=") + quotedString("type") + Literal(">") + SkipTo(Literal("</i>"))+ Literal("</i>")
location_pattern = get_location_pattern()
row_pattern = get_td_pattern()


# %%
from tqdm.notebook import tqdm
import json
import os

def parse_change_log(file_path):
    file_name = os.path.splitext(os.path.split(file_path)[-1])[0]
    with open(file_path, 'r', encoding='utf-8') as f:
        data = f.read()
        results = {}
        for row in tqdm(row_pattern.searchString(data)):
            entity_match = entity_with_link.searchString(row.entity.strip())
            if entity_match:
                for entity_match_row in entity_match:
                    entity = {
                        "name": entity_match_row.entity_name,
                        "link": entity_match_row.link.strip("\"")
                    }
            else:
                entity = {
                    "name": row.entity.strip(),
                    "link": None
                }
            
            if type_match := type_pattern.searchString(row.type.strip()):
                for type_match_row in type_match:
                    type = type_match_row.type.strip("\"")
            else:
                type = row.type.strip()
            
            location_detailed = {}
            if location_match := location_pattern.searchString(row.location.strip()):
                
                for location_match_row in location_match:
                    location_match_row = location_match_row.asDict()
                    
                    if location_match_row.get("where_rule"):
                        location_detailed["type"] = "where_rule"
                        location_detailed["rule_name"] = location_match_row.get("rule_name", "")
                        location_detailed["rule_change"] = location_match_row.get("rule_change", "")
                    elif location_match_row.get("property"):
                        location_detailed["type"] = "property"
                        location_detailed["property_name"] = location_match_row.get("property_name", "")
                    elif location_match_row.get("supertype"):
                        location_detailed["type"] = "supertype"
                    elif location_match_row.get("item"):
                        location_detailed["type"] = "item"
                        location_detailed["item_name"] = location_match_row.get("item_name", "")
                    elif location_match_row.get("inverse_attribute"):
                        location_detailed["type"] = "inverse_attribute"
                        location_detailed["attribute_name"] = location_match_row.get("attribute_name", "")
                        location_detailed["attribute_change"] = location_match_row.get("attribute_change", "")
                    elif location_match_row.get("direct_attribute"):
                        location_detailed["type"] = "direct_attribute"
                        location_detailed["attribute_name"] = location_match_row.get("attribute_name", "")
                        location_detailed["attribute_change"] = location_match_row.get("attribute_change", "")
                    elif location_match_row.get("deprecated"):
                        location_detailed["type"] = "deprecated"
                    elif location_match_row.get("abstract"):
                        location_detailed["type"] = "abstract"
                    elif location_match_row.get("applicability"):
                        location_detailed["type"] = "applicability"
                    elif location_match_row.get("type"):
                        location_detailed["type"] = "type"
                    elif location_match_row.get("unique_rule"):
                        location_detailed["type"] = "unique_rule"
                    else:
                        raise ParseException("Unknown type")
            
            if entity["name"] not in results:
                results[entity["name"]] = {
                    "link": entity["link"],
                    "changes": []
                }
            results[entity["name"]]["changes"].append({
                "type": type,
                "location": row.location.strip(),
                "location_detailed": location_detailed,
                "description": row.description.strip()
            })
    if not os.path.isdir("./outputs/change_log_jsons"):
        os.mkdir("./outputs/change_log_jsons")
    with open(f"./outputs/change_log_jsons/{file_name}.json", "w") as f:
        json.dump(results, f, ensure_ascii=False, indent=4)
        
for file in tqdm(os.listdir("./resources/change_logs")):
    parse_change_log(f"./resources/change_logs/{file}")

# %%
with open("./outputs/ifc4_change_log.json", "r") as f:
    data = json.load(f)
# %%
print(len(set([row["type"] for row in data["change_logs"]])))
# %%
