from owlready2 import *
from Activity import AGActivity, extractActivity
from Scenario import AGScenario
from UInterface import clear

ontoprefix = "covid19planner."

onto_path.append(".")
onto = get_ontology("covid19planner.owl")
onto.load()

locationsText = {"Consuming": "Go eat/drink something",
    "Leisure": "Other activities",
    "Sports": "Sports"}

locations = ["Bookshop", "Boutique", "Cafe", "Library", "Restaurant", "Shop", "Stadium"]

#activities = list(activityText.keys())

if __name__ == "__main__":
    clear()
    mainact = extractActivity(main=True, entranceText="Hello and welcome to your personal COVID-19 awareness assistant!\nLet us know, what kind of activity did you wish to do?", onto=onto, locations=locations)
    scenario = AGScenario(onto=onto, act=mainact)
    scenario.toOnto()
    clear()
    for el in scenario.toOnto().hasUser:
        print("\t" + str(el.hasHealth))

    close_world(mainact.mainAgent, Properties=[onto.hasKnownCOVID], recursive=False)
    if mainact.companions is not None:
        for comp in mainact.companions:
            close_world(comp.toOnto(), Properties=[onto.hasKnownCOVID], recursive=False)
    close_world(scenario.toOnto(), Properties=[onto.hasUser], recursive=False)

    # for debug purposes
    #onto.save()

    with onto:
        sync_reasoner()

    clear()
    if scenario.isUnsafe():
        print("I'm afraid I think this is very unsafe, you should probably not go.\n")
    elif scenario.isSafe():
        print("I find no issue with your plan! I think it's fine to go!\n")
    else:
        print("Mmm... I can not assure you that your plan is safe, but it isn't horribly risky. If you go, I wouldn't find it wrong, but be aware that you do so at your own risk.\n")
