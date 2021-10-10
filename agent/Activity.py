from owlready2 import *
from UInterface import userMenu, clear
from Person import AGPerson, extractPerson
from Location import extractLocation
from Transportation import extractTransportation

texts = {True:{
            "present":{
                "companionsbegin":"Alright! Tell me about who's accompanying you (if any). Are you going to be alone at the {place}? (yes/no): ",
                "companionsmore":"Are you going with anybody else? (yes/no): "},
            "past":{
                "companionsbegin":"Alright! Tell me about who accompanied you (if any). Were you alone at the {place}? (yes/no): ",
                "companionsmore":"Did you go with anybody else? (yes/no): "}},

         False:{
            "present":{
                "companionsbegin":"Alright! Tell me about who accompanyied them (if any). Were they alone at the {place}? (yes/no): ",
                "companionsmore":"Did they go with anybody else? (yes/no): "},
            "past":{
                "companionsbegin":"Alright! Tell me about who accompanyied them (if any). Were they alone at the {place}? (yes/no): ",
                "companionsmore":"Did they go with anybody else? (yes/no): "}}}

class AGActivity:

    def __init__(self, name, typeonto, loc, actonto):
        self.name = name
        self.loc = loc
        self.otype = typeonto
        self.actonto = actonto
        self.mainAgent = None
        self.companions = None
        self.loconto = None

    def setAgent(self, person):
        self.mainAgent = person.toOnto()

    def toOnto(self, onto, main=False):
        if main:
            self.mainAgent.isGoingToLocation.append(self.loconto)
        else:
            self.mainAgent.hasGoneToLocation.append(self.loconto)
        if self.companions is not None:
            if main:
                for comp in self.companions:
                    comp.toOnto().isGoingToLocation.append(self.loconto)
            else:
                for comp in self.companions:
                    comp.toOnto().hasGoneToLocation.append(self.loconto)

def extractActivity(main=False, entranceText=None, onto=None, locations=None, time="present", agent=None):
    if entranceText is None or onto is None or locations is None:
        raise Exception("Parameters found None")

    clear()

    print(entranceText)

    uindex = userMenu(locations)
    loc = onto.search_one(iri="*"+locations[uindex])
    act = loc.hasActivity[0]
    acttypeonto = act.is_a[0]

    act = AGActivity(acttypeonto.name, acttypeonto, loc, act)
    clear()
    if agent is None:
        agent = extractPerson(main=main, onto=onto, name=loc.name)
    act.setAgent(agent)

    loc = extractLocation(main=main, onto=onto, loconto=loc, activity=acttypeonto, time=time)
    loconto = loc.toOnto()
    act.loconto = loconto

    comps = extractCompanions(main=main, loc=loc, onto=onto, time=time)
    act.companions = comps

    act.toOnto(onto, main=main)

    trans = extractTransportation(main=main, onto=onto, personname=agent.name, placename=loc.originalname, time=time)
    if time == "present":
        agent.trans = trans
    else:
        agent.pastTransps.append(trans)
    agent.updateTransps()

    return act


def extractCompanions(main=False, loc=None, onto=None, time=time):
    clear()
    companions = []
    while(True):
        resp = input(texts[main][time]["companionsbegin"].format(place=loc.originalname))
        if resp.lower() == "yes":
            return None
        elif resp.lower() == "no":
            break
        else:
            print("Please input yes or no")
    while(True):
        clear()
        comp = extractPerson(main=False, onto=onto, functType="companions", name=loc.originalname)
        comp.trans = extractTransportation(main=False, onto=onto, personname=comp.name, placename=loc.originalname, time=time)
        companions.append(comp)
        clear()
        while(True):
            resp = input(texts[main][time]["companionsmore"])
            if resp.lower() == "yes":
                break
            elif resp.lower() == "no":
                return companions
            else:
                print("Please input yes or no")
