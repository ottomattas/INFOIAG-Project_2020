from UInterface import clear, userMenu
from Ontology import generateRandomIri

texts = {True:{
            "present":{
                "transpstart":"Alright! How are you going to go to the {place}?\n"},
            "past":{
                "transpstart":"Alright! How did you go to the {place}?\n"
                }},

         False:{
            "past":{
                "transpstart":"Alright! How did {name} go to the {place}?\n"},
            "present":{
                "transpstart":"Alright! How is {name} going to the {place}?\n"}}}

transps = [("Alone.", "Individual_Transportation"),
           ("Accompanied.", "Group_Transportation")]

class AGTransportation:

    def __init__(self, onto):
        self.onto = onto
        self.trans = None
        self.transonto = None

    def toOnto(self):
        if self.transonto is not None:
            return self.transonto
        elif self.trans is None:
            return None
        else:
            self.transonto = self.onto.search_one(iri="*"+self.trans)
            return self.transonto

def extractTransportation(main=False, onto=None, personname=None, placename=None, time="present"):
    clear()
    print(texts[main][time]["transpstart"].format(name=personname, place=placename))

    tra = AGTransportation(onto)
    uindex = userMenu([x[0] for x in transps]+["I don't know."])
    if uindex < len(transps):
        tra.trans = transps[uindex][1]

    return tra
