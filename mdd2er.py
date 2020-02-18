import os
import ntpath
import re
from parser import Parser
import sys

###########################################################################################################
## This script analyzes the subfolder and file structure of the Data Definition folder, that should
## contain MDD and IDD files that describe the database schema.
## The structure is converted to a graph shows hierarchy relation (as nodes into clusters) and
## foreign key relation (as arrows going from a node to its foreign keys).
###########################################################################################################


if (len(sys.argv) != 1):
	print("Syntax to be used:")
	print("  python mdd2er.py <path-to-mdds-directory>")
	print(" ")
	exit()

# PARAMETERS -------------------------------------------------

# root of the tree to analyze (relative or absolute path)
BASE_PATH = sys.argv[1] #"../../best/graphMaker/testmdds"
# file where to write the generated code
OUT_FILENAME = 'codeGenerated.py'

#-------------------------------------------------------------

# open in append mode
f = open("./"+OUT_FILENAME, 'a')

p = Parser(BASE_PATH, f)

# clear file
f.truncate(0)

# write first lines
f.write("from graphviz import Digraph\n")
f.write("\n")
f.write(p.getGraphName()+" = Digraph('G', filename='graph.gv')\n")
f.write(p.getGraphName()+".attr(compound='true')\n")


# where the magic happens
p.recursiveSearch()


# write last lines
f.write("\n")
f.write(p.getGraphName()+".view()\n")

f.close()

# run the drawing script
import codeGenerated