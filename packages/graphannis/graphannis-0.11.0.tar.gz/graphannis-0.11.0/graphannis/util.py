import networkx as nx
import sys, re

def salt_uri_from_match(match):
    elements = re.split('::', match, 3)
    if len(elements) == 3:
        return elements[2]
    elif len(elements) == 2:
        return elements[1]
    else:
        return elements[0]

