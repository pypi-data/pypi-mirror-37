# CFGraph - RDF Collections flattener for `rdflib`
[![Pyversions](https://img.shields.io/pypi/pyversions/CFGraph.svg)](https://pypi.python.org/pypi/CFGraph)
[![PyPi](https://img.shields.io/pypi/v/CFGraph.svg)](https://pypi.python.org/pypi/CFGraph)

## Revision History
* 0.1.0 - Initial drop
* 0.2.0 - Functionality overhaul

An implementation of a [`rdflib`](https://github.com/RDFLib/rdflib)[`Graph`](https://rdflib.readthedocs.io/en/stable/apidocs/rdflib.html#rdflib.graph.Graph)
that reads well-formed RDF collections as lists.

## Requirements
* Python 3.6 -- this module uses the new typing annotations
* [`rdflib`](https://github.com/RDFLib/rdflib) -- a Python library for working with RDF

## Use
See [Jupyter notebook](README.ipynb)

## Notes
This is a read-only interface.  It does *not* convert list style representations into collections.

This module assumes that collections are "well formed", as determined by common convention.  (*Why the RDF WG did
not put a stake in the gound on this remains a mystery*).  By "well formed" we mean:
+ Empty list:  `:s :p rdf:nil.`
+ Single element:  `:s :p _:b1 . _:b1 rdf:first :o; rdf:rest rdf:nil`
+ Every list (`_:n`) in a list will have *exactly* two entries, `_:n rdf:first .` and `_:n rdf:rest [_:n2 or rdf:nil]`

In addition, we impose the restriction:
* The subject of `rdf:first` or `rdf:rest` is always a blank node.

The output for RDF Collections that do not conform to the above rules is not predictable.