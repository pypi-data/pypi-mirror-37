# -*- coding: utf-8 -*-

import re
import os.path
import json
import rdflib
import ast
from helpers import printp
from evaluator import *

class Ontology:

	def __init__(self, ontologyLocation, prefix):
		self.ontologyLocation = ontologyLocation
		if self.__validateOntologyLocation():
			self.prefix = prefix
			self.ontology_raw = self.__importOntologyRaw()
			self.ontology = self.__importOntology()
			self.prefixes = self.__getPrefixes()
			self.classes = self.__getClasses2()
			self.classes2 = self.__getClasses2()
			self.objectProperties = self.__getObjectProperties()
			self.objectProperties2 = self.__getObjectProperties2()
			self.dataProperties = self.__getDataProperties()
			self.dataProperties2 = self.__getDataProperties2()
		else:
			print("File not Found!")

	def __validateOntologyLocation(self):
		return os.path.isfile(self.ontologyLocation)

	def __importOntologyRaw(self):
		fd = open(self.ontologyLocation, "r")
		read_data = []
		for line in fd:
			read_data.append(line)
		fd.close()
		return read_data

	def __importOntology(self):
		g=rdflib.Graph()
		g.load(self.ontologyLocation, format='turtle')
		j =  g.serialize(format = "json-ld")
		j = ast.literal_eval(j)
		return evaluateOntology(j)

	def __getPrefixes(self):
		prefixes = {}
		prefix_with_seperator = {}

		for line in self.ontology_raw:
			if '@prefix' in line:
				line = ''.join(line.split())
				prefix = line[7: line.find(":")]
				source = line[line.find("<")+1 : line.find(">")]
				prefixes[prefix] = source

				if prefix in self.prefix:
					element = {prefix : source[-1:]}
					prefix_with_seperator.update(element)

		self.test = prefix_with_seperator

		return prefixes

	def __getClasses(self, separator = "/"):
		classList = []
		for key in self.ontology.keys():
			className = key[key.rfind(separator)+1:]
			# print className
			if className:
				if "#Class" in self.ontology[key]["rdf:type"]:
					classList.append(className)
		return classList

	def __getClasses2(self):
		classes = {}
		for prefix in self.test:
			for key in self.ontology.keys():
				separator = self.test[prefix]
				className = key[key.rfind(separator)+1:]
				if self.prefixes[prefix] in key:
					if className:
						if "#Class" in self.ontology[key]["rdf:type"]:
							classes.setdefault(prefix,[]).append(className)

		return classes

	def __hasSubClasses(self, className):
		subClasses = []
		for nodeName in self.ontology:
			node = self.ontology[nodeName]
			if "http://www.w3.org/2002/07/owl#Class" in node["rdf:type"]:
				if "http://www.w3.org/2000/01/rdf-schema#subClassOf" in node.keys():
					superClasses = node["http://www.w3.org/2000/01/rdf-schema#subClassOf"]
					for superClass in superClasses:
						if isinstance(superClass, dict):
							if "http://www.w3.org/2002/07/owl#Class" in superClass["rdf:type"]:
								for names in superClass.values():
									if isinstance(names, list):
										for name in names:
											if className == name:
												subClasses.append(nodeName)
						if isinstance(superClass, str):
							if superClass == className:
								subClasses.append(nodeName)
		return subClasses

	def __getObjectProperties(self, separator = "/"):
		objectProperties = {}
		for key in self.ontology.keys():
			className = key[key.rfind("/")+1:]
			if className:
				if "#ObjectProperty" in self.ontology[key]["rdf:type"]:
					domainClasses = []
					if "http://www.w3.org/2000/01/rdf-schema#domain" in self.ontology[key]:
						for domain in self.ontology[key]["http://www.w3.org/2000/01/rdf-schema#domain"]:
							domainClasses.append(domain)
							for subClass in self.__hasSubClasses(domain):
								domainClasses.append(subClass)

					rangeClasses = []
					if "http://www.w3.org/2000/01/rdf-schema#range" in self.ontology[key]:
						for rangeName in self.ontology[key]["http://www.w3.org/2000/01/rdf-schema#range"]:
							rangeClasses.append(rangeName)
							for subClass in self.__hasSubClasses(rangeName):
								rangeClasses.append(subClass)

					domainDict = {"domain" : domainClasses}
					rangeDict = {"range" : rangeClasses}
					objectProperties.update({className : domainDict})
					objectProperties[className].update(rangeDict)
		return objectProperties

	def __getObjectProperties2(self, separator = "/"):
		objectProperties = {}
		for prefix in self.test:
			for key in self.ontology.keys():
				separator = self.test[prefix]
				className = key[key.rfind(separator)+1:]
				if self.prefixes[prefix] in key:
					if className:
						if "#ObjectProperty" in self.ontology[key]["rdf:type"]:
							domainClasses = []
							if "http://www.w3.org/2000/01/rdf-schema#domain" in self.ontology[key]:
								for domain in self.ontology[key]["http://www.w3.org/2000/01/rdf-schema#domain"]:
									domainClasses.append(domain)
									for subClass in self.__hasSubClasses(domain):
										domainClasses.append(subClass)

							rangeClasses = []
							if "http://www.w3.org/2000/01/rdf-schema#range" in self.ontology[key]:
								for rangeName in self.ontology[key]["http://www.w3.org/2000/01/rdf-schema#range"]:
									rangeClasses.append(rangeName)
									for subClass in self.__hasSubClasses(rangeName):
										rangeClasses.append(subClass)

							domainDict = {"domain" : domainClasses}
							rangeDict = {"range" : rangeClasses}
							prop = {}
							prop.setdefault(className,{}).update(domainDict)
							prop.setdefault(className,{}).update(rangeDict)

							objectProperties.setdefault(prefix, {}).update(prop)
		return objectProperties

	def __getDataProperties(self, separator = "/"):
		dataProperties = {}
		for key in self.ontology.keys():
			className = key[key.rfind("/")+1:]
			if className:
				if "#DatatypeProperty" in self.ontology[key]["rdf:type"]:
					domainClasses = []
					if "http://www.w3.org/2000/01/rdf-schema#domain" in self.ontology[key]:
						for domain in self.ontology[key]["http://www.w3.org/2000/01/rdf-schema#domain"]:
							domainClasses.append(domain)
							for subClass in self.__hasSubClasses(domain):
								domainClasses.append(subClass)

					rangeClasses = []
					if "http://www.w3.org/2000/01/rdf-schema#range" in self.ontology[key]:
						for rangeName in self.ontology[key]["http://www.w3.org/2000/01/rdf-schema#range"]:
							rangeClasses.append(rangeName)
							for subClass in self.__hasSubClasses(rangeName):
								rangeClasses.append(subClass)

					domainDict = {"domain" : domainClasses}
					rangeDict = {"range" : rangeClasses}
					dataProperties.update({className : domainDict})
					dataProperties[className].update(rangeDict)
		return dataProperties

	def __getDataProperties2(self, separator = "/"):
		dataProperties = {}
		for prefix in self.test:
			for key in self.ontology.keys():
				separator = self.test[prefix]
				className = key[key.rfind(separator)+1:]
				if self.prefixes[prefix] in key:
					if className:
						if "#DatatypeProperty" in self.ontology[key]["rdf:type"]:
							domainClasses = []
							if "http://www.w3.org/2000/01/rdf-schema#domain" in self.ontology[key]:
								for domain in self.ontology[key]["http://www.w3.org/2000/01/rdf-schema#domain"]:
									domainClasses.append(domain)
									for subClass in self.__hasSubClasses(domain):
										domainClasses.append(subClass)

							rangeClasses = []
							if "http://www.w3.org/2000/01/rdf-schema#range" in self.ontology[key]:
								for rangeName in self.ontology[key]["http://www.w3.org/2000/01/rdf-schema#range"]:
									rangeClasses.append(rangeName)
									for subClass in self.__hasSubClasses(rangeName):
										rangeClasses.append(subClass)

							domainDict = {"domain" : domainClasses}
							rangeDict = {"range" : rangeClasses}

							prop = {}
							prop.setdefault(className,{}).update(domainDict)
							prop.setdefault(className,{}).update(rangeDict)

							dataProperties.setdefault(prefix, {}).update(prop)
		return dataProperties

	def isClass(self, element):
		found = False
		for key in self.classes:
			if element in self.classes[key]:
				found = True
		return found

	def isObjectProperty(self, element):
		return element in self.objectProperties

	def isObjectProperty2(self, element):
		found = False
		for key in self.objectProperties2:
			if element in self.objectProperties2[key]:
				found = True
		return found

	def isDataProperty(self, element):
		return element in self.dataProperties

	def isDataProperty2(self, element):
		found = False
		for key in self.dataProperties2:
			if element in self.dataProperties2[key]:
				found = True
		return found

	def isDefined(self, element):
		for dataProperty, value in self.dataProperties.items():
			for value in value["domain"]:
				if element in value:
					return True
		return False

	def printOntology(self, raw = False):
		if raw:
			for line in self.ontology_raw:
				print(line)
		else:
			print json.dumps(self.ontology, indent=2, sort_keys=True)

	def getPrefixForProperty(self, properties, property_name):
		for key in properties:
			if property_name in properties[key].keys():
				return key

	def getPrefixForClass(self, class_name):
		for key in self.classes:
			if class_name in self.classes[key]:
				return key

	# KEEP THIS! If two different prefixes have the same class, the correct prefix has to be fetched
	# def getPrefixForClass2(self, class_name, ontologyURI):
	# 	print "\t" + ontologyURI
	# 	for key in self.classes:
	# 		print "\t\t" + key
	# 		if (class_name in self.classes[key]) and (ontologyURI in self.prefixes[key]):
	# 			print key
	# 			print ontologyURI
	# 			return key



	# Function to use when expanding to ontology http import

	# def __validateOntologyLocation(self):
	# 	regex = re.compile(r'^(http:\/\/www\.|https:\/\/www\.|http:\/\/|https:\/\/)?[a-z0-9]+([\-\.]{1}[a-z0-9]+)*\.[a-z]{2,5}(:[0-9]{1,5})?(\/.*)?$', re.IGNORECASE)
	# 	if os.path.isfile(self.ontologyLocation) == True:
	# 		return False
	# 	elif (re.match(regex, self.ontologyLocation) is not None) == True:
	# 		return True
	# 	else:
	# 		return None