from UInterface import clear, multiUserMenu
from Ontology import generateRandomIri

texts = {True:"Alright! Are you bringing any protective gear to the {place}?\n",
         False:"Alright! Is {name} bringing any protective gear to the {place}?\n"}

gears = [("Facemask.", "Facemask"),
           ("Disinfectant liquid.", "Disinfectant"),
           ("Protective glasses/goggles.", "Glasses"),
           ("Plastic gloves.", "Gloves"),
           ("Respirator.", "Respirator")]

class AGProtectionGear:

    def __init__(self, onto):
        self.onto = onto
        self.gears = None
        self.gearsonto = None

    def toOnto(self):
        if self.gearsonto is not None:
            return self.gearsonto
        elif self.gears is None:
            return None
        else:
            self.gearsonto = []
            for gear in self.gears:
                self.gearsonto.append(self.onto.search_one(iri="*"+gear))
            return self.gearsonto

def extractProtectionGear(main=False, onto=None, personname=None, placename=None):
    clear()

    uindexes = multiUserMenu([x[0] for x in gears], textprompt=texts[main].format(name=personname, place=placename))

    gear = AGProtectionGear(onto)
    gear.gears = [gears[x][1] for x in uindexes]

    return gear.toOnto()
