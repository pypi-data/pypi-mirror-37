# CFGraph - RDF Collections flattener for `rdflib`
[![Pyversions](https://img.shields.io/pypi/pyversions/CFGraph.svg)](https://pypi.python.org/pypi/sparql_slurper)
[![PyPi](https://version-image.appspot.com/pypi/?name=CFGraph)](https://pypi.python.org/pypi/sparql_slurper)

## Revision History
* 0.1.0 - Initial drop

An implementation of a [`rdflib`](https://github.com/RDFLib/rdflib)[`Graph`](https://rdflib.readthedocs.io/en/stable/apidocs/rdflib.html#rdflib.graph.Graph)
that reads well-formed RDF collections as lists.

## Requirements
* Python 3.6 -- this module uses the new typing annotations
* [`rdflib`](https://github.com/RDFLib/rdflib) -- a Python library for working with RDF

## Use
See [Jupyter notebook](README.ipynb)

## Issues and notes
* We need to add reverse functions (`predicate_objects`, etc.)