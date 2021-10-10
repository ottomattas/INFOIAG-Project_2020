from Ontology import generateRandomIri

class AGScenario():

    def __init__(self, onto=None, act=None):
        self.onto = onto
        self.act = act
        self.scenarioclass = self.onto.search_one(iri="*Scenario")
        self.safeclass = self.onto.search_one(iri="*Safe")
        self.unsafeclass = self.onto.search_one(iri="*Unsafe")
        self.users = []
        self.scenarioonto = None
        if act.mainAgent is not None:
            self.users.append(act.mainAgent)
        if act.companions is not None:
            for comp in act.companions:
                self.users.append(comp.toOnto())

    def toOnto(self):
        if self.scenarioonto is not None:
            return self.scenarioonto
        self.scenarioonto = self.scenarioclass(generateRandomIri(self.onto), hasUser=self.users)
        return self.scenarioonto

    def isSafe(self):
        return self.safeclass in self.scenarioonto.is_a

    def isUnsafe(self):
        return self.unsafeclass in self.scenarioonto.is_a
