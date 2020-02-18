import os
import ntpath
from pathlib import Path
import re
from parser import Parser
import sys

###########################################################################################################
## This script analyzes the subfolder and file structure of the Data Definition folder, that should
## contain MDD and IDD files that describe the database schema.
## The structure is converted to a graph shows hierarchy relation (as nodes into clusters) and
## foreign key relation (as arrows going from a node to its foreign keys).
###########################################################################################################


if (len(sys.argv) < 2):
	print("Syntax to be used:")
	print("  python mdd2er.py <path-to-mdds-directory> [depth-limit (default=10)]")
	print(" ")
	exit()



# PARAMETERS -------------------------------------------------

# root of the tree to analyze (relative or absolute path)
MDDS_PATH = sys.argv[1] #"../../best/graphMaker/testmdds"

OUTPUT_PATH = "./output/"

# file where to write the generated code
OUTPUT_SCRIPT = 'codeGenerated.py'

# depth limit in the graph
if (len(sys.argv) == 3):
	depth_limit = int(sys.argv[2])
	if (depth_limit < 1):
		print("Depth limit should be an integer >= 1")
		exit()
else:
	depth_limit = 10

OUTPUT_GRAPH = "graph_d" + str(depth_limit) + ".gv"

#-------------------------------------------------------------

# create output directory if it does not exist
Path(OUTPUT_PATH).mkdir(parents=True, exist_ok=True)

# open in append mode
f = open(OUTPUT_SCRIPT, 'a')

p = Parser(MDDS_PATH, f, depth_limit)

# clear file
f.truncate(0)

# write first lines
f.write("from graphviz import Digraph\n")
f.write("\n")
f.write(p.getGraphName()+" = Digraph('G', filename='"+OUTPUT_PATH+OUTPUT_GRAPH+"')\n")
f.write(p.getGraphName()+".attr(compound='true')\n")


# where the magic happens
p.recursiveSearch()


# write last lines
f.write("\n")
f.write(p.getGraphName()+".view()\n")

f.close()

# run the drawing script
import codeGenerated