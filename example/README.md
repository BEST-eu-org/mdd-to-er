# Example

Here is presented a mock database schema, with some generic company, archive and so on.

# Run

Run the following lines:

```
python mdd2er.py ./examples/dataDefinitions/ 1
python mdd2er.py ./examples/dataDefinitions/ 2
python mdd2er.py ./examples/dataDefinitions/ 3
python mdd2er.py ./examples/dataDefinitions/
```

The results are saved as PDF files.

# Results explaination

The script is run on the data definition structure, using different levels of "depth limit".

- Each node of the graph represents a MDD file (or a directory).
- Each arrow between 2 nodes represents a dependency between the first node and the second one: it means that the source node contains a foreign key pointing to the destination node.
- Sometimes it is possible to see rectangles surrounding several nodes: they represent the directory containing those nodes.

When depth limit is 1, only the top-level directories are shown (and they are shown as nodes, although being directories). Anyway all the arrows of the children are not hidden, they are instead shown as arrows starting from the top-level node. The destination of the arrow is also a top-level node, accordingly to the depth limit set.

Whith depth limit equal to 2 and 3 we can see an increment in the level of details, since also the non-top-level directories are shown. When depth limit parameter is not specified, it is automatically set to 10. Please note that for this simple database schema there is no difference between the diagrams with depth 3 and 10.

Finally, please note that some nodes are shown even if they do not exist in our directory structure. This is because some MDD files refer to those nodes, that are external to our directory. This nodes are shown like normal nodes, but their name represents also the hierarchical position in the external data definition. For example a node called "fruits_red_Apple" may correspond to the external file "fruit/red/Apple.mdd".