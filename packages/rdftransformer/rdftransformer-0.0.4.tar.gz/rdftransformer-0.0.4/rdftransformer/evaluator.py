# -*- coding: utf-8 -*-

def extractNodeName(node):
	return node["@id"]

def extractNodeType(node):
	# printp(node["@type"])
	return node["@type"][0]

def elementIsName(element):
	return True if "@id" in element else False

def elementIsType(element):
	return True if "@type" in element else False


# TODO: @list type -> see intersectionOf
def evaluateElement(node, element):
	root = node[element]
	length = len(root)
	idlist = []
	values = {}
	for parent in root:
		for child in parent:
			# print element
			child_key = ""
			child_value = ""

			if "@id" in child:
				child_value = parent["@id"]
				idlist.append(child_value)

			if "@list" in child:
				for listElement in parent[child]:
					if "@value" in listElement.keys()[0]:
						idlist.append(listElement["@value"])
					if "@id" in listElement.keys()[0]:
						idlist.append(listElement["@id"])

			if "@type" in child:
				child_key = "type"
				child_value = parent["@type"]
				values.update({child_key : child_value})

			if "@language" in child:
				child_key = "language"
				child_value = parent["@language"]
				values.update({child_key : child_value})

			if "@value" in child:
				child_key = "value"
				child_value = parent["@value"]
				values.update({child_key : child_value})
			# print child_value
	if len(values):
		return {element : values}
	else:
		return {element : idlist}


def substituteNodes(ontology):
	substituted = {}
	for node in ontology:
		if "_:" not in node:
			temp = {node: ontology[node]}
			for key in temp:
				if isinstance(temp[key], dict):
					i = 0
					for k in temp[key]:
						if isinstance(temp[key][k], list):
							i = 0
							for listElement in temp[key][k]:
								if "_:" in listElement:
									temp[key][k][i] = ontology[temp[key][k][i]]
								i += 1
			substituted.update(temp)
	return substituted

def evaluateOntology(ontology):
	evaluated = {}
	for node in ontology:
		evaluatedNode = {}
		nodename = extractNodeName(node)
		nodetype = extractNodeType(node)
		# print nodename
		for element in node:
			if (elementIsType(element) == False) and (elementIsName(element) == False):
				evaluatedNode.update(evaluateElement(node, element))
		evaluatedNode.update({"rdf:type" : nodetype})
		evaluated.update({nodename : evaluatedNode})
		# print "\n"
	return substituteNodes(evaluated)