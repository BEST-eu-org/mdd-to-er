import os
import re

class Parser:
	
	# root of the tree to analyze, it does NOT contain the final "/"
	base_path = ""
	# file where to write the generated code
	out_file = None
	# depth limit
	depth_limit = 10

	# Constructor
	def __init__(self, base_path, out_file, depth_limit=10):
		self.base_path = base_path
		if (self.base_path[-1] == "/"):
			self.base_path = self.base_path[:-1]
		self.out_file = out_file
		self.depth_limit = depth_limit


	def getGraphName(self):
		return self.rpa2cluster([])


	# rpa: relative path array (one element per each folder in the relative path from base_path)
	# returns: relative path string (inclding the base_path)
	def rpa2path(self, rpa):
		return self.base_path + "/" + "/".join(rpa)


	# rpa: relative path array (one element per each folder in the relative path from base_path)
	# returns: full name of the node in the generated code (not label)
	def rpa2node(self, rpa):
		return "_".join(rpa)


	# rpa: relative path array (one element per each folder in the relative path from base_path)
	# returns: full name of the cluster in the generated code (not label)
	def rpa2cluster(self, rpa):
		# We must include "cluster" at the beginning of the name to let graphviz understand it is a subgraph and
		# not a node. It's a requirement of the library.
		# Ther root graph will be named just "cluster".
		if (rpa == []):
			return "cluster"
		else:
			return "cluster" + "_" + "_".join(rpa)


	# rpa: relative path array (one element per each folder in the relative path from base_path)
	# returns: the same rpa but without extension it is a file
	def rpaRemoveExtension(self, rpa):
		nameAndExtension = rpa[-1].split(".")
		if (len(nameAndExtension) > 1):
			name = ".".join(nameAndExtension[:-1])
			rpa[-1] = name 	# remove extension
		return rpa


	# rpa: relative path array (one element per each folder in the relative path from base_path)
	# returns: the extension of the rpa point to a file, otherwise None
	def rpaGetExtension(self, rpa):
		nameAndExtension = rpa[-1].split(".")
		if (len(nameAndExtension) > 1):
			ext = nameAndExtension[-1]
		else:
			ext = None
		return ext


	# rpa: relative path array (one element per each folder in the relative path from base_path)
	# description: 
	def recursiveSearch(self, rpa=[]):

		for filename in os.listdir(self.rpa2path(rpa)):
			rpa_child = rpa.copy()
			rpa_child.append(filename)

			path = self.rpa2path(rpa_child)
			depth_level = len(rpa_child)
			print("Analyzing", path)

			# if it is a directory
			if (os.path.isdir(path)):

				if (depth_level < self.depth_limit):
					self.generateSubgraph(rpa_child)

				self.recursiveSearch(rpa_child)
			
			# if it is a file
			else:
				
				ext = self.rpaGetExtension(rpa_child)
				if (ext == "mdd" or ext == "idd"):

					# the smallest cluster allowed by the depth limit that contains the child under analysis
					nearestParent = rpa_child[:self.depth_limit]
					# generate the node for the nearest parent (multiple nodes will be rendered only once)
					self.generateNode(self.rpaRemoveExtension(nearestParent))
					
					# detect foreign keys in the analyzed file
					destNodeList = self.getDestinationsList(self.rpaRemoveExtension(rpa_child), ext)
					# replace each destination with its own nearest parent
					for idx, destNode in enumerate(destNodeList):
						if (len(destNode) > self.depth_limit):
							destNodeList[idx] = destNode[:self.depth_limit]
					
					# generate all the edges starting from ne nearest parent
					self.generateEdges(self.rpaRemoveExtension(nearestParent), destNodeList)


	# rpa: relative path array (one element per each folder in the relative path from base_path)
	# description: 
	def generateSubgraph(self, rpa):

		ind_lv = len(rpa) - 1						# code indentation level
		subgraphLabel = rpa[-1]
		subgraphName = self.rpa2cluster(rpa)
		parentName = self.rpa2cluster(rpa[:-1])

		self.out_file.write("\n")
		# write instruction to create a subgraph
		self.out_file.write(("    "*ind_lv) + "with "+parentName+".subgraph(name='"+subgraphName+"') as "+subgraphName+":\n")
		# write instruction to give a label to the subgraph
		self.out_file.write(("    "*(ind_lv+1)) + subgraphName+".attr(label='"+subgraphLabel+"')\n")


	# rpa: relative path array (one element per each folder in the relative path from base_path)
	# description: 
	def generateNode(self, rpa):
			
		ind_lv = len(rpa) - 1						# code indentation level
		nodeLabel = rpa[-1]
		nodeName = self.rpa2node(rpa)
		parentName = self.rpa2cluster(rpa[:-1])

		self.out_file.write("\n")
		# write instruction to create the node
		self.out_file.write(("    "*ind_lv) + parentName+".node(name='"+nodeName+"', label='"+nodeLabel+"')\n")


	# rpa: relative path array (one element per each folder in the relative path from base_path)
	# description: 
	def generateEdges(self, rpa_source, destNodeList):

		ind_lv = len(rpa_source) - 1						# code indentation level
		nodeName = self.rpa2node(rpa_source)
		
		# for each foreign key write an instruction to draw an arrow to it
		for destNode in destNodeList:
			destNodeName = self.rpa2node(destNode)
			if (nodeName != destNodeName):
				self.out_file.write(("    "*ind_lv) + self.rpa2cluster([])+".edge('"+nodeName+"', '"+destNodeName+"')\n")


	# rpa: relative path array (one element per each folder in the relative path from base_path)
	# extension: extension of the file to open (.mdd or .idd)
	# returns: a list of rpa's, each one representing a node to which the current file is referring with a pointer
	def getDestinationsList(self, rpa, extension):

		# open the file in read mode
		f = open(self.rpa2path(rpa)+"."+extension, "r")

		destinations_list = []
		
		for line in f.readlines():
			# remove possible strings
			for match in re.finditer("\".*\"", line):
				line = line[:match.start()] + line[match.end():]
			
			# remove possible comments
			position = line.find("#")
			if (position >= 0):
				line = line[:position+1]
			position = line.find(";")
			if (position >= 0):
				line = line[:position]

			# if the line is in the form "attribute = ptr foreign.key.node"
			match1 = re.search(".*= *ptr .+", line)
			# if the line is in the form "attribute = set foreign.key.node"
			match2 = re.search(".*= *set .+", line)
			# if the line is in the form "attribute->!include=foreign.key.node"
			match3 = re.search(".*->!include *= *.+", line)

			if (match1):
				line = line[line.find("ptr")+3:]	# remove all the initial part
				line = list(filter(None, re.split(" |\t|\n|;.*\n|=", line)))
				if (len(line) > 0):
					destinations_list.append(line[0])
				continue

			if (match2):
				line = line[line.find("set")+3:]	# remove all the initial part
				line = list(filter(None, re.split(" |\t|\n|;.*\n|=", line)))
				if (len(line) > 0 and ("." in line[0])):		# the second check is to avoid things like "set int{}" or "set float{}"
					destinations_list.append(line[0])
				continue
			
			if (match3):
				line = line[line.find("!include")+len("!include"):]	# remove all the initial part
				line = list(filter(None, re.split(" |\t|\n|;.*\n|=", line)))
				if (len(line) > 0):
					destinations_list.append(line[0])
				continue

		f.close()

		destinations_list_rpa = []
		for dest in destinations_list:
			dest = dest.split(".")
			destinations_list_rpa.append(dest)

		return destinations_list_rpa