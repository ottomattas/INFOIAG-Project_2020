from owlready2 import *
from Ontology import generateRandomIri
from UInterface import userMenu, clear

texts = {"present":
            {"ventilation":"Alright! Please tell me about the {name}. How well ventilated is it?\n",
                "distancing":"Does the {name} enforce strict distancing rules?\n"},

         "past":
            {"ventilation":"Alright! Please tell me about the {name}. How well ventilated was it?\n",
                "distancing":"Did the {name} enforce strict distancing rules?\n"}}

textsmain = {True:{
                "eatingwhere":"Where do you plan to eat?\n",
                "groupseating":"Do you know if they enforce a strict seating etiquette at the {name}?\n"},

              False:{
                "eatingwhere":"Do you know where they ate?\n",
                "groupseating":"Do you know if they enforced a strict seating etiquette at the {name}?\n"}}

ventilation = [("It's well ventilated.", "Good_Ventilation"),
               ("It's not very well ventilated.", "Bad_Ventilation")]

distancing = [("Yes.","Proper_Distancing"),
              ("No.","Improper_Distancing")]

eating_where = [("Outside.","Outdoor_seating"),
                ("Inside.","Indoor_seating"),
                ("Just takeaway.","Takeaway")]

seating = [("They don't allow multiple people to sit together.","Seating_Single"),
           ("They only allow up to two people to sit together at most.","Seating_Double"),
           ("They allow more than two people to sit together.","Seating_Group")]

class AGLocation:

    def __init__(self, loconto, onto):
        self.onto = onto
        self.loconto = None
        self.locationclass = onto.search_one(iri="*Location")
        self.originalname = loconto.name
        self.activity = loconto.hasActivity
        self.ventilation = None
        self.distancing = None
        self.eating_where = None
        self.seating = None

    def toOnto(self):
        if self.loconto is not None:
            return self.loconto
        self.loconto = self.locationclass(generateRandomIri(self.onto), hasActivity=self.activity)
        elements = [self.ventilation, self.distancing, self.eating_where, self.seating]
        for el in elements:
            if el is not None:
                ontoel = self.onto.search_one(iri="*"+el)
                self.loconto.hasLocationParameter.append(ontoel)
        return self.loconto


def extractLocation(main=False, onto=None, functType=None, loconto=None, activity=None, time="present"):
    clear()

    loc = AGLocation(loconto, onto)

    print(texts[time]["ventilation"].format(name=loconto.name))
    uindex = userMenu(list([x[0] for x in ventilation])+["I don't know."])
    if uindex < len(ventilation):
        loc.ventilation = ventilation[uindex][1]

    clear()
    print(texts[time]["distancing"].format(name=loconto.name))
    uindex = userMenu(list([x[0] for x in distancing])+["I don't know."])
    if uindex < len(distancing):
        loc.distancing = distancing[uindex][1]

    if activity.name == "Consuming":
        clear()
        print(textsmain[main]["eatingwhere"])
        uindex = userMenu(list([x[0] for x in eating_where])+["I don't know."])
        if uindex < len(eating_where):
            loc.eating_where = eating_where[uindex][1]

        clear()
        print(textsmain[main]["groupseating"].format(name=loconto.name))
        uindex = userMenu(list([x[0] for x in seating])+["I don't know."])
        if uindex < len(seating):
            loc.seating = seating[uindex][1]

    return loc
