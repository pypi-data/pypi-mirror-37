from typing import NamedTuple, Union, Tuple, Optional, Generator

from rdflib import Graph, URIRef, Literal, BNode, RDF
from rdflib.collection import Collection
from rdflib.exceptions import UniquenessError

QueryTriple = Tuple[Optional[URIRef], Optional[URIRef], Optional[Union[Literal, URIRef]]]


class RDFTriple(NamedTuple):
    s: Union[URIRef, BNode] = None
    p: URIRef = None
    o: Union[Literal, URIRef, BNode] = None


class CFGraph(Graph):
    """ Collection Flattening Graph

    Collections are returned as lists of triples
    """

    def __init__(self, *args, **kwargs) -> None:
        self._inside = False
        super().__init__(*args, **kwargs)

    def triples(self, pattern: QueryTriple) -> Generator[RDFTriple, None, None]:
        if not self._inside:
            try:
                self._inside = True
                subj, pred, _ = pattern
                try:
                    obj = super().value(subj, pred, any=False)
                except UniquenessError:
                    obj = None
                if obj and super().value(obj, RDF.first):
                    for e in Collection(self, obj):
                        yield (pattern[0], pattern[1], e)
                elif obj == RDF.nil:
                    return
                else:
                    for t in super().triples(pattern):
                        yield t
            finally:
                self._inside = False
        else:
            for t in super().triples(pattern):
                yield t
