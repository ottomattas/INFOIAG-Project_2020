class Agent:
    __instance__ = None

    def __init__(self):
        self.people = {}

        if Agent.__instance__ is None:
            Agent.__instance__ = self
        else:
            raise Exception("Agent is singleton")

    def addPerson(self, person):
        self.people[person.name] = person

    @staticmethod
    def globalAgent():
        if not Agent.__instance__:
            Agent()
        return Agent.__instance__
