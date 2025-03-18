# Test app for IFC change logs
import streamlit as st
from streamlit_extras.grid import grid as st_grid
import rdflib
from chage_log_ontology.namespace import CHANGE_LOG, CHANGE_LOG_INST
from ifc_change_log_explorer.render import TableRenderer
from ifc_change_log_explorer.query_engine import QueryEngine

st.set_page_config(layout="wide")

if st.session_state.get("ifc_schema_version", None) is None:
    st.session_state["ifc_schema_version"] = "IFC4.1"
if st.session_state.get("graph", None) is None:
    G = rdflib.Graph()
    G.parse("./outputs/change_log_ttls/ifc4.1_change_log.ttl")
    st.session_state["graph"] = G

with st.sidebar:
    with st.form("file_selector_form", border=False):
        option = st.selectbox(
            "Select a IFC version",
            options=["IFC4", "IFC4.1", "IFC4.2", "IFC4.3.2"],
            index=1,
        )
        submit = st.form_submit_button("Load data", use_container_width=True)
    if submit:
        G = rdflib.Graph()
        G.parse(f"./outputs/change_log_ttls/{option.lower()}_change_log.ttl")
        st.session_state["graph"] = G
        st.session_state["ifc_schema_version"] = option
        # st.success(f"Loaded {option} data")
    st.metric(label="Number of triples", value=len(st.session_state["graph"]))

st.title(f"{st.session_state['ifc_schema_version']} Change Log")
G = st.session_state["graph"]

query_engine = QueryEngine(G)
# placeholder = st.empty()


# filter_option = grid.selectbox("Filter", ["type", "entity"])

grid = st_grid([2,2,1])
filter_by_entity = grid.text_input("Entity filter", "")
mode = grid.radio("change_mode", ["all", "create", "delete", "edit"], horizontal=True)
style_id = grid.radio("style", [1, 2, 3], horizontal=True)
undefined_loc = st.checkbox("undefined location only", value=False)

if st.session_state.get("results", None) is None or st.session_state.get("mode", None) != mode or st.session_state.get("filter_by_entity", None) != filter_by_entity:
    st.session_state["mode"] = mode
    st.session_state["filter_by_entity"] = filter_by_entity
    st.session_state["results"] = query_engine.query(mode=mode, entity_keyword=filter_by_entity)

selected_entities = st.multiselect("entities", sorted(list(set([item.entity_label for item in st.session_state["results"]]))))
selected_results = [item for item in st.session_state["results"] if item.entity_label in selected_entities] if selected_entities else st.session_state["results"]
renderer = TableRenderer(selected_results)

st.markdown(renderer.render(style_id=style_id, undefined_loc=undefined_loc), unsafe_allow_html=True)
