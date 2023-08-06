# -*- coding: utf-8 -*-

import re
import os.path
import json
import string, random
from helpers import isDate
from helpers import printp
from ontology import Ontology
from coordinates import UTM
from lxml import etree as ET
from rdflib import Graph, Namespace, Literal, URIRef, BNode, collection
from rdflib import RDF, RDFS, OWL, XSD


class Annotation:

	def __init__(self):
		self.graph = Graph()
		self.indent = 0
		self.depth = 0


	def importOntology(self, ontologyLocation, prefix = []):
		self.ontology = Ontology(ontologyLocation, prefix)

		self.__addNamespaces()
		return self.ontology

	def importData(self, filename):
		if self.__validateDataLocation(filename):
			# self.namespaces = self.__getNamespaces(filename)
			self.data = ET.parse(filename)
			self.root = self.data.getroot()
			self.namespaces = self.root.nsmap
			self.baseNamespace = self.namespaces[None]
		else:
			print ("File not found!")
		return self.data

	def getElementsByTagName(self, tag, parent = "", namespaces = {}):
		tagPrefix = self.__getPrefixFromTag(tag)
		tagName =  self.__getNameFromTag(tag)

		parentPrefix = self.__getPrefixFromTag(parent)
		parentName = self.__getNameFromTag(parent)


		if not namespaces:
			if tagPrefix in self.namespaces:
				tagQuery =  "{" + self.namespaces[tagPrefix] + "}" + tagName
			else:
				tagQuery = tagName

			if parentPrefix in self.namespaces:
				parentQuery = "{" + self.namespaces[parentPrefix] + "}" + parentName
			else:
				parentQuery = parentName
		else:
			print (namespaces[tagPrefix])
			if tagPrefix in namespaces:
				tagQuery = "{" + namespaces[tagPrefix] + "}" + tagName
			else:
				tagQuery = tagName

			if parentPrefix in namespaces:
				parentQuery =  "{" + namespaces[parentPrefix] + "}" + parentName
			else:
				parentQuery = parentName

		query = ".//"

		if not parent:
			query = query + tagQuery
		else:
			query = query + parentQuery + "/" + tagQuery

		return self.root.findall(query)

		# TODO
		# def getElementByAttribute()



	def printRecur(self, root):
		"""Recursively prints the tree."""
		print (' '*self.indent + '%s: %s' % (root.tag, root.attrib.get('name', root.text)))
		self.indent += 4
		for elem in root.getchildren():
			self.printRecur(elem)
			self.indent -= 4


	def __getCurveID(self, ring, curveMember):
		curve = ring[curveMember].getchildren()[0]
		return curve.attrib["{http://www.opengis.net/gml/3.2}id"]

	def __getCurvePosList(self, ring, curveMember):
		curve = ring[curveMember].getchildren()[0]
		segment = curve.getchildren()[0]
		lineStringSegment = segment.getchildren()[0]
		posList = lineStringSegment.getchildren()[0]
		pos_list = posList.text.split(" ")
		return pos_list


	def __alkisAnnotate(self, element, uid):
		tag = self.__getNameFromTag(element.tag, "}")
		children = element.getchildren()
		surface = children[0]
		if "{http://www.opengis.net/gml/3.2}Surface" in surface.tag:
			multiPolygon_id = children[0].attrib["{http://www.opengis.net/gml/3.2}id"]
			self.graph.add((self.ontologyNamespaces["alkis"][uid], self.ontologyNamespaces["alkis"]["position"], self.ontologyNamespaces["alkis"][uid + "_" + "position"]))
			self.graph.add((self.ontologyNamespaces["alkis"][uid + "_" + "position"], RDF.type, self.ontologyNamespaces["ngeo"]["MultiPolygon"]))
			self.graph.add((self.ontologyNamespaces["alkis"][uid + "_" + "position"], self.ontologyNamespaces["ngeo"]["id"], Literal(multiPolygon_id)))
			children = surface.getchildren()
			patches = children[0]
			if "{http://www.opengis.net/gml/3.2}patches" in patches.tag:
				children = patches.getchildren()
				polygonPatch = children[0]
				if "{http://www.opengis.net/gml/3.2}PolygonPatch" in polygonPatch.tag:
					self.graph.add((self.ontologyNamespaces["alkis"][uid + "_" + "polygonMember"], RDF.type, self.ontologyNamespaces["ngeo"]["Polygon"]))

					children = polygonPatch.getchildren()

					for element in children:
						if element.tag in "{http://www.opengis.net/gml/3.2}exterior":
							exterior_children = element.getchildren()
							ring = exterior_children[0]
							if ring.tag in "{http://www.opengis.net/gml/3.2}Ring":
								ring_child = ring.getchildren()
								point_list = []
								linearRing = BNode()
								posList = BNode()
								points = []
								plist = [BNode()]
								for x in range(0, len(ring_child)):
									lat = self.__getCurvePosList(ring_child, x)[0]
									lon = self.__getCurvePosList(ring_child, x)[1]
									utm = UTM(32, "n", float(lat) , float(lon))
									coordinates = utm.toLatLon()
									if x == 0:
										id1 = self.__getCurveID(ring_child, 0)
										id2 = self.__getCurveID(ring_child, len(ring_child)-1)
										point = BNode()
										self.graph.add((point, self.ontologyNamespaces["geo"]["lat"], Literal(str(coordinates[0]))))
										self.graph.add((point, self.ontologyNamespaces["geo"]["long"], Literal(str(coordinates[1]))))
										self.graph.add((point, self.ontologyNamespaces["ngeo"]["id"], Literal(id1)))
										self.graph.add((point, self.ontologyNamespaces["ngeo"]["id"], Literal(id2)))
										self.graph.add((posList, RDF.first, point))
										points.append(point)
										if len(ring_child) > 1:
											self.graph.add((posList, RDF.rest, plist[x]))
										else:
											self.graph.add((posList, RDF.rest, RDF.nil))

									else:
										id1 = self.__getCurveID(ring_child, x-1)
										id2 = self.__getCurveID(ring_child, x)

										point = BNode()
										self.graph.add((point, self.ontologyNamespaces["geo"]["lat"], Literal(str(coordinates[0]))))
										self.graph.add((point, self.ontologyNamespaces["geo"]["long"], Literal(str(coordinates[1]))))
										self.graph.add((point, self.ontologyNamespaces["ngeo"]["id"], Literal(id1)))
										self.graph.add((point, self.ontologyNamespaces["ngeo"]["id"], Literal(id2)))
										points.append(point)
										self.graph.add((plist[x-1], RDF.first, points[x]))


										if (x+1) < len(ring_child):
											plist.append(BNode())
											self.graph.add((plist[x-1], RDF.rest, plist[x]))
										else:
											self.graph.add((plist[x-1], RDF.rest, RDF.nil))
									
									# point_list.append([coordinates[0], coordinates[1], [id1, id2]])
									
								collection.Collection(self.graph,posList)
								self.graph.add((linearRing, RDF.type, self.ontologyNamespaces["ngeo"]["LinearRing"]))
								self.graph.add((linearRing, self.ontologyNamespaces["ngeo"]["posList"], posList))

							self.graph.add((self.ontologyNamespaces["alkis"][uid + "_" + "polygonMember"], self.ontologyNamespaces["ngeo"]["exterior"], linearRing))
							self.graph.add((self.ontologyNamespaces["alkis"][uid + "_" + "position"], self.ontologyNamespaces["ngeo"]["polygonMember"], self.ontologyNamespaces["alkis"][uid + "_" + "polygonMember"]))

	def __alkisAnnotatePoint(self, element, uid):
		children = element.getchildren()
		point = children[0]
		if "{http://www.opengis.net/gml/3.2}Point" in point.tag:
			point_id = children[0].attrib["{http://www.opengis.net/gml/3.2}id"]
			self.graph.add((self.ontologyNamespaces["alkis"][uid], self.ontologyNamespaces["alkis"]["objektkoordinaten"], self.ontologyNamespaces["alkis"][uid + "_objektkoordinaten"]))
			position = point.getchildren()[0].text.split(" ")
			utm = UTM(32, "n", float(position[0]), float(position[1]))
			location = utm.toLatLon()
			# print location
			self.graph.add((self.ontologyNamespaces["alkis"][uid + "_objektkoordinaten"], RDF.type, self.ontologyNamespaces["ngeo"]["Point"]))
			self.graph.add((self.ontologyNamespaces["alkis"][uid + "_objektkoordinaten"], self.ontologyNamespaces["geo"]["lat"], Literal(str(location[0]))))
			self.graph.add((self.ontologyNamespaces["alkis"][uid + "_objektkoordinaten"], self.ontologyNamespaces["geo"]["lon"], Literal(str(location[1]))))
			self.graph.add((self.ontologyNamespaces["alkis"][uid + "_objektkoordinaten"], self.ontologyNamespaces["ngeo"]["id"], Literal(point_id)))





	def annotate(self, element, depth = 0, uid = ""):
		# print ("==========")
		# print ("%i:%s" % (depth, element.tag))
		tag = self.__getNameFromTag(element.tag, "}")
		if tag == "position":
			self.__alkisAnnotate(element, uid)
			return
		if tag == "objektkoordinaten":
			self.__alkisAnnotatePoint(element, uid)
			return
		

		if (self.ontology.isClass(tag)) and (depth == 0):
			# print "Class: " + tag
			uid = self.__getIdentifier(element)
			prefix = self.ontology.getPrefixForClass(tag)
			self.graph.add((self.ontologyNamespaces[prefix][uid], RDF.type, self.ontologyNamespaces[prefix][tag]))


		if self.ontology.isObjectProperty2(tag):
			# print ("ObjectProperty: " + tag)
			property_prefix = self.ontology.getPrefixForProperty(self.ontology.objectProperties2, tag)
			# print (element.getparent().tag)
			children = element.getchildren()
			if len(children):
				o_domain = uid + "_" + tag
				o_range = self.__getNameFromTag(children[0].tag, "}")
				full = children[0].tag
				onto = full[full.find("{")+1:full.find("}")]
				if self.__inPrefixes(onto):
					range_prefix = self.ontology.getPrefixForClass(o_range)

					if self.ontology.isDefined(o_range) and (range_prefix != None):
						self.graph.add((self.ontologyNamespaces[property_prefix][uid], self.ontologyNamespaces[property_prefix][tag], self.ontologyNamespaces[property_prefix][o_domain]))
						self.graph.add((self.ontologyNamespaces[property_prefix][o_domain], RDF.type, self.ontologyNamespaces[range_prefix][o_range]))



		if self.ontology.isDataProperty2(tag):
			# print ("DataProperty: " + tag)
			prefix = self.ontology.getPrefixForProperty(self.ontology.dataProperties2, tag)
			d_domain = self.ontology.dataProperties2[prefix][tag]["domain"]
			# print (self.ontology.dataProperties[tag]["domain"][0])
			for domain in d_domain:
				for s,p,o in self.graph.triples( (None, None, URIRef(domain)) ):
					if uid in s:
						if isDate(element.text):
   							self.graph.add((s, self.ontologyNamespaces[prefix][tag], Literal(element.text, datatype=XSD.date)))
   						else:
   							self.graph.add((s, self.ontologyNamespaces[prefix][tag], Literal(element.text))) 

   			
		# print ("==========")
		for elem in element.getchildren():
			depth += 1
			self.annotate(elem, depth, uid)
			depth -= 1

	def output(self, destination = None, format = "turtle"):
		if not destination:
			print self.graph.serialize(format = format)
		else:
			print "Saving to " + destination + "..."
			self.graph.serialize(destination = destination, format = format)
			print "Successfully saved."
		self.graph = Graph()
		self.addNamespaces()

	def __getPrefixFromTag(self, tag, separator = ":"):
		if separator in tag:
			prefix = tag[:tag.find(separator)]
			return prefix
		else:
			return None

	def __getNameFromTag(self, tag, separator = ":"):
		if separator in tag:
			name = tag[tag.find(separator) + 1 : ]
			return name
		else:
			return tag

	def __getIdentifier(self, element):
		for elem in element.getchildren():
			if self.namespaces["gml"] in elem.tag:
				return elem.text
			else:
				return self.__generateUniqueID(element)

	def __generateUniqueID(self, element):
		x = ''.join(random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for _ in range(16))
		return "urn:adv:oid:" + x

	def __getNamespaces(self):
		namespaces = {}
		for name in self.ontology.prefixes:
			if (name == "owl") or (name == "xsd") or (name == "rdf") or (name == "rdfs"):
				continue
			else:
				namespaces[name] = Namespace(self.ontology.prefixes[name])
		self.ontologyNamespaces = namespaces
		return namespaces

	def __addNamespaces(self):
		for name_space, path in self.__getNamespaces().items():
			self.graph.bind(name_space, path)

	def addNamespaces(self):
		for name_space, path in self.__getNamespaces().items():
			self.graph.bind(name_space, path)

	def __inPrefixes(self, ontologyURI):
		if (ontologyURI in self.ontology.prefixes.values()) or (ontologyURI in self.baseNamespace):
			return True

		return False

	def __validateDataLocation(self, filename):
		return os.path.isfile(filename)