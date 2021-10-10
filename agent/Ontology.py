from owlready2 import *
import string, random

def generateRandomIri(onto):
    letters = string.ascii_letters + string.digits
    res = ''.join(random.choice(letters) for i in range(10))
    while(onto.search_one(iri="*"+res) is not None):
        res = ''.join(random.choice(letters) for i in range(10))
    return res
