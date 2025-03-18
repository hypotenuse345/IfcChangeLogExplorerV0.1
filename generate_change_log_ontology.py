from rdflib import Graph, Literal, BNode, URIRef, RDF, RDFS, OWL, XSD
from rdflib.namespace import XSD
from rdflib.collection import Collection

from chage_log_ontology.ontology import define_ontology
from chage_log_ontology.namespace import CHANGE_LOG, bind_prefixes

# 初始化Graph
G = Graph()
bind_prefixes(G)
define_ontology(G)

# Classes
G.add((CHANGE_LOG.BaseChange, RDF.type, OWL.Class))
G.add((CHANGE_LOG.BaseChange, RDFS.label, Literal("BaseChange")))
G.add((CHANGE_LOG.BaseChange, RDFS.comment, Literal("BaseChange is the base class for all changes.")))

G.add((CHANGE_LOG.Create, RDF.type, OWL.Class))
G.add((CHANGE_LOG.Create, RDFS.label, Literal("Create")))
G.add((CHANGE_LOG.Create, RDFS.comment, Literal("Create is a change that adds a new element to the ontology.")))
G.add((CHANGE_LOG.Create, RDFS.subClassOf, CHANGE_LOG.BaseChange))
G.add((CHANGE_LOG.Create, CHANGE_LOG.data_feather, Literal("plus-square")))

G.add((CHANGE_LOG.Delete, RDF.type, OWL.Class))
G.add((CHANGE_LOG.Delete, RDFS.label, Literal("Delete")))
G.add((CHANGE_LOG.Delete, RDFS.comment, Literal("Delete is a change that removes an element from the ontology.")))
G.add((CHANGE_LOG.Delete, RDFS.subClassOf, CHANGE_LOG.BaseChange))
G.add((CHANGE_LOG.Delete, CHANGE_LOG.data_feather, Literal("x-square")))

G.add((CHANGE_LOG.Update, RDF.type, OWL.Class))
G.add((CHANGE_LOG.Update, RDFS.label, Literal("Update")))
G.add((CHANGE_LOG.Update, RDFS.comment, Literal("Update is a change that modifies an element in the ontology.")))
G.add((CHANGE_LOG.Update, RDFS.subClassOf, CHANGE_LOG.BaseChange))
G.add((CHANGE_LOG.Update, CHANGE_LOG.data_feather, Literal("edit")))

G.add((CHANGE_LOG.SchematicConcept, RDF.type, OWL.Class))
G.add((CHANGE_LOG.SchematicConcept, RDFS.label, Literal("Concept")))
G.add((CHANGE_LOG.SchematicConcept, RDFS.comment, Literal("Concept is a class that represents a concept in the ontology.")))

G.add((CHANGE_LOG.ChangeLocation, RDF.type, OWL.Class))
G.add((CHANGE_LOG.ChangeLocation, RDFS.label, Literal("ChangeLocation")))
G.add((CHANGE_LOG.ChangeLocation, RDFS.comment, Literal("ChangeLocation is a class that represents the location of a change.")))

G.add((CHANGE_LOG.EntityChangeLocation, RDF.type, OWL.Class))
G.add((CHANGE_LOG.EntityChangeLocation, RDFS.label, Literal("EntityChangeLocation")))
G.add((CHANGE_LOG.EntityChangeLocation, RDFS.comment, Literal("EntityChangeLocation is a class that represents the change location of an entity.")))
G.add((CHANGE_LOG.EntityChangeLocation, RDFS.subClassOf, CHANGE_LOG.ChangeLocation))

G.add((CHANGE_LOG.PSetChangeLocation, RDF.type, OWL.Class))
G.add((CHANGE_LOG.PSetChangeLocation, RDFS.label, Literal("PSetChangeLocation")))
G.add((CHANGE_LOG.PSetChangeLocation, RDFS.comment, Literal("PSetChangeLocation is a class that represents the change location of a property set template.")))
G.add((CHANGE_LOG.PSetChangeLocation, RDFS.subClassOf, CHANGE_LOG.ChangeLocation))

G.add((CHANGE_LOG.EnumChangeLocation, RDF.type, OWL.Class))
G.add((CHANGE_LOG.EnumChangeLocation, RDFS.label, Literal("EnumChangeLocation")))
G.add((CHANGE_LOG.EnumChangeLocation, RDFS.comment, Literal("EnumChangeLocation is a class that represents the change location of an enumeration.")))
G.add((CHANGE_LOG.EnumChangeLocation, RDFS.subClassOf, CHANGE_LOG.ChangeLocation))

G.add((CHANGE_LOG.DeprecatedChangeLoc, RDF.type, OWL.Class))
G.add((CHANGE_LOG.DeprecatedChangeLoc, RDFS.label, Literal("DeprecatedChangeLocation")))
G.add((CHANGE_LOG.DeprecatedChangeLoc, RDFS.comment, Literal("DeprecatedChangeLocation is a class that represents the location of a change in a deprecated element.")))
G.add((CHANGE_LOG.DeprecatedChangeLoc, RDFS.subClassOf, CHANGE_LOG.ChangeLocation))

G.add((CHANGE_LOG.AbstractChangeLoc, RDF.type, OWL.Class))
G.add((CHANGE_LOG.AbstractChangeLoc, RDFS.label, Literal("AbstractChangeLocation")))
G.add((CHANGE_LOG.AbstractChangeLoc, RDFS.comment, Literal("AbstractChangeLocation is a class that represents the abstract location of a change.")))
G.add((CHANGE_LOG.AbstractChangeLoc, RDFS.subClassOf, CHANGE_LOG.EntityChangeLocation))

G.add((CHANGE_LOG.ApplicabilityChangeLoc, RDF.type, OWL.Class))
G.add((CHANGE_LOG.ApplicabilityChangeLoc, RDFS.label, Literal("ApplicabilityChangeLocation")))
G.add((CHANGE_LOG.ApplicabilityChangeLoc, RDFS.comment, Literal("ApplicabilityChangeLocation is a class that represents the location of a change in an application.")))
G.add((CHANGE_LOG.ApplicabilityChangeLoc, RDFS.subClassOf, CHANGE_LOG.PSetChangeLocation))

G.add((CHANGE_LOG.SupertypeChangeLoc, RDF.type, OWL.Class))
G.add((CHANGE_LOG.SupertypeChangeLoc, RDFS.label, Literal("SupertypeChangeLocation")))
G.add((CHANGE_LOG.SupertypeChangeLoc, RDFS.comment, Literal("SupertypeChangeLocation is a class that represents the location of a change in a supertype.")))
G.add((CHANGE_LOG.SupertypeChangeLoc, RDFS.subClassOf, CHANGE_LOG.EntityChangeLocation))

G.add((CHANGE_LOG.TypeChangeLoc, RDF.type, OWL.Class))
G.add((CHANGE_LOG.TypeChangeLoc, RDFS.label, Literal("TypeChangeLocation")))
G.add((CHANGE_LOG.TypeChangeLoc, RDFS.comment, Literal("TypeChangeLocation is a class that represents the location of a change in a type.")))
G.add((CHANGE_LOG.TypeChangeLoc, RDFS.subClassOf, CHANGE_LOG.PSetChangeLocation))

G.add((CHANGE_LOG.DirectAttributeChangeLoc, RDF.type, OWL.Class))
G.add((CHANGE_LOG.DirectAttributeChangeLoc, RDFS.label, Literal("DirectAttributeChangeLocation")))
G.add((CHANGE_LOG.DirectAttributeChangeLoc, RDFS.comment, Literal("DirectAttributeChangeLocation is a class that represents the location of a change in an attribute.")))
G.add((CHANGE_LOG.DirectAttributeChangeLoc, RDFS.subClassOf, CHANGE_LOG.EntityChangeLocation))

G.add((CHANGE_LOG.InverseAttributeChangeLoc, RDF.type, OWL.Class))
G.add((CHANGE_LOG.InverseAttributeChangeLoc, RDFS.label, Literal("InverseAttributeChangeLocation")))
G.add((CHANGE_LOG.InverseAttributeChangeLoc, RDFS.comment, Literal("InverseAttributeChangeLocation is a class that represents the location of a change in an inverse attribute.")))
G.add((CHANGE_LOG.InverseAttributeChangeLoc, RDFS.subClassOf, CHANGE_LOG.EntityChangeLocation))

G.add((CHANGE_LOG.ItemChangeLoc, RDF.type, OWL.Class))
G.add((CHANGE_LOG.ItemChangeLoc, RDFS.label, Literal("ItemChangeLocation")))
G.add((CHANGE_LOG.ItemChangeLoc, RDFS.comment, Literal("ItemChangeLocation is a class that represents the location of a change in an item.")))
G.add((CHANGE_LOG.ItemChangeLoc, RDFS.subClassOf, CHANGE_LOG.EnumChangeLocation))

G.add((CHANGE_LOG.PropertyChangeLoc, RDF.type, OWL.Class))
G.add((CHANGE_LOG.PropertyChangeLoc, RDFS.label, Literal("PropertyChangeLocation")))
G.add((CHANGE_LOG.PropertyChangeLoc, RDFS.comment, Literal("PropertyChangeLocation is a class that represents the location of a change in a property.")))
G.add((CHANGE_LOG.PropertyChangeLoc, RDFS.subClassOf, CHANGE_LOG.PSetChangeLocation))

G.add((CHANGE_LOG.WhereRuleChangeLoc, RDF.type, OWL.Class))
G.add((CHANGE_LOG.WhereRuleChangeLoc, RDFS.label, Literal("WhereRuleChangeLocation")))
G.add((CHANGE_LOG.WhereRuleChangeLoc, RDFS.comment, Literal("WhereRuleChangeLocation is a class that represents the location of a change in a where rule.")))
G.add((CHANGE_LOG.WhereRuleChangeLoc, RDFS.subClassOf, CHANGE_LOG.EntityChangeLocation))

G.add((CHANGE_LOG.UniqueRuleChangeLoc, RDF.type, OWL.Class))
G.add((CHANGE_LOG.UniqueRuleChangeLoc, RDFS.label, Literal("UniqueRuleChangeLocation")))
G.add((CHANGE_LOG.UniqueRuleChangeLoc, RDFS.comment, Literal("UniqueRuleChangeLocation is a class that represents the location of a change in a where rule.")))
G.add((CHANGE_LOG.UniqueRuleChangeLoc, RDFS.subClassOf, CHANGE_LOG.EntityChangeLocation))


G.add((CHANGE_LOG.UndefinedChangeLoc, RDF.type, OWL.Class))
G.add((CHANGE_LOG.UndefinedChangeLoc, RDFS.label, Literal("UndefinedChangeLocation")))
G.add((CHANGE_LOG.UndefinedChangeLoc, RDFS.comment, Literal("UndefinedChangeLocation is a class that represents the location of a change that is not defined.")))
G.add((CHANGE_LOG.UndefinedChangeLoc, RDFS.subClassOf, CHANGE_LOG.ChangeLocation))

# DataType Properties
G.add((CHANGE_LOG.data_feather, RDF.type, OWL.DatatypeProperty))
G.add((CHANGE_LOG.data_feather, RDFS.label, Literal("data feather")))
G.add((CHANGE_LOG.data_feather, RDFS.comment, Literal("data feather is a property that represents the data feather of a change.")))
G.add((CHANGE_LOG.data_feather, RDFS.domain, CHANGE_LOG.BaseChange))
G.add((CHANGE_LOG.data_feather, RDFS.range, XSD.string))

G.add((CHANGE_LOG.description, RDF.type, OWL.DatatypeProperty))
G.add((CHANGE_LOG.description, RDFS.label, Literal("description")))
G.add((CHANGE_LOG.description, RDFS.comment, Literal("description is a property that represents the description of a change.")))
G.add((CHANGE_LOG.description, RDFS.domain, CHANGE_LOG.BaseChange))
G.add((CHANGE_LOG.description, RDFS.range, XSD.string))

G.add((CHANGE_LOG.link, RDF.type, OWL.DatatypeProperty))
G.add((CHANGE_LOG.link, RDFS.subPropertyOf, RDFS.seeAlso))
G.add((CHANGE_LOG.link, RDFS.label, Literal("link")))
G.add((CHANGE_LOG.link, RDFS.comment, Literal("link is a property that represents the link of a concept.")))
G.add((CHANGE_LOG.link, RDFS.domain, CHANGE_LOG.SchematicConcept))
G.add((CHANGE_LOG.link, RDFS.range, XSD.string))

G.add((CHANGE_LOG.changed, RDF.type, OWL.DatatypeProperty))
G.add((CHANGE_LOG.changed, RDFS.label, Literal("changed")))
G.add((CHANGE_LOG.changed, RDFS.comment, Literal("changed is a property that represents the changed concept.")))
G.add((CHANGE_LOG.changed, RDFS.domain, CHANGE_LOG.ChangeLocation))
G.add((CHANGE_LOG.changed, RDFS.range, XSD.string))

# Object Property
G.add((CHANGE_LOG.hasChange, RDF.type, OWL.ObjectProperty))
G.add((CHANGE_LOG.hasChange, RDFS.label, Literal("hasChange")))
G.add((CHANGE_LOG.hasChange, RDFS.comment, Literal("hasChange is a property that represents the change of a concept.")))
G.add((CHANGE_LOG.hasChange, RDFS.domain, CHANGE_LOG.SchematicConcept))
G.add((CHANGE_LOG.hasChange, RDFS.range, CHANGE_LOG.BaseChange))

G.add((CHANGE_LOG.isChangeOf, RDF.type, OWL.ObjectProperty))
G.add((CHANGE_LOG.isChangeOf, RDFS.label, Literal("isChangeOf")))
G.add((CHANGE_LOG.isChangeOf, RDFS.comment, Literal("isChangeOf is a property that represents the concept of a change.")))
G.add((CHANGE_LOG.isChangeOf, RDFS.domain, CHANGE_LOG.BaseChange))
G.add((CHANGE_LOG.isChangeOf, RDFS.range, CHANGE_LOG.SchematicConcept))
G.add((CHANGE_LOG.isChangeOf, OWL.inverseOf, CHANGE_LOG.hasChange))

G.add((CHANGE_LOG.hasLocation, RDF.type, OWL.ObjectProperty))
G.add((CHANGE_LOG.hasLocation, RDFS.label, Literal("hasLocation")))
G.add((CHANGE_LOG.hasLocation, RDFS.comment, Literal("hasLocation is a property that represents the location of a change.")))
G.add((CHANGE_LOG.hasLocation, RDFS.domain, CHANGE_LOG.BaseChange))
G.add((CHANGE_LOG.hasLocation, RDFS.range, CHANGE_LOG.ChangeLocation))

G.add((CHANGE_LOG.isLocationOf, RDF.type, OWL.ObjectProperty))
G.add((CHANGE_LOG.isLocationOf, RDFS.label, Literal("isLocationOf")))
G.add((CHANGE_LOG.isLocationOf, RDFS.comment, Literal("isLocationOf is a property that represents the location of a change.")))
G.add((CHANGE_LOG.isLocationOf, RDFS.domain, CHANGE_LOG.ChangeLocation))
G.add((CHANGE_LOG.isLocationOf, RDFS.range, CHANGE_LOG.BaseChange))
G.add((CHANGE_LOG.isLocationOf, OWL.inverseOf, CHANGE_LOG.hasLocation))

# Save the ontology to a file
G.serialize(destination="change_log_ontology.ttl", format="turtle")
