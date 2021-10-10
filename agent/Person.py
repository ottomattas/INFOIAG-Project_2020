from owlready2 import *
from UInterface import userMenu, multiUserMenu, clear
from Agent import Agent as ag
from ProtectiveGear import extractProtectionGear
import Activity as AC

texts = {True:{"age":"How old are you?: ",
            "gender":"What is your gender?: ",
            "covidtest":"What was the result of your test?: ",
            "weight":"Under which weight type do you fall?: ",
            "smokes":"Do you smoke? (yes/no): ",
            "symptoms":"What symptoms do you have?",
            "diseases":"What serious diseases do you have?",
            "liveswith":"Perfect! Do you wish to share who you live with? This information is important to value risk at home. (yes/no): ",
            "liveswithintroduce":"Alright! Tell me about a person you live with, what is their name?: ",
            "furtherliveswith":"Alright! Do you wish to tell me about someone else you live with? (yes/no): ",
            "companionsintroduce":"Alright! Tell me about this companion, what is their name?: ",
            "pastactivityyesno":"Have you gone to other places earlier that might be relevant? (yes/no): ",
            "pastactivitytell":"Alright! Tell me, where did you go?\n"},

         False:{"age":"How old is {name}?: ",
            "gender":"What is {name}'s gender?: ",
            "covidtest":"What was the result of {name}'s test?: ",
            "weight":"Under which weight type does {name} fall?: ",
            "smokes":"Does {name} smoke? (yes/no): ",
            "symptoms":"What symptoms does {name} have?",
            "diseases":"What serious diseases does {name} have?",
            "liveswith":"Perfect! Do you know who {name} lives with? (yes/no): ",
            "liveswithintroduce":"Alright! Tell me about a person {name} lives with, what is their name?: ",
            "furtherliveswith":"Alright! Do you recall anybody else who lives with {name}? (yes/no): ",
            "companionsintroduce":"Alright! Tell me about this companion, what is their name?: ",
            "pastactivityyesno":"Has {name} gone to other places earlier that might be relevant? (yes/no): ",
            "pastactivitytell":"Alright! Tell me, where did {name} go?\n"}}

def getAge(main, person):
    age = input(texts[main]["age"].format(name=person.name))
    age = int(age)
    if age < 18:
        person.age = "Child"
    elif age > 65:
        person.age = "Old"
    else:
        person.age = "Adult"

def getGender(main, person):
    genders = ["Male", "Female"]
    print(texts[main]["gender"].format(name=person.name))
    uindex = userMenu(genders)
    person.gender = genders[uindex]

def covidTest(main, person):
    testvalues = [("Positive", "Positive_Test"), ("Negative", "Negative_Test")]
    print(texts[main]["covidtest"].format(name=person.name))
    uindex = userMenu([x[0] for x in testvalues])
    person.covidtest = testvalues[uindex][1]

def getWeight(main, person):
    weightvalues = [("Underweight", "Underweight"), ("On expected weight", "On_Weight"), ("Overweight", "Overweight")]
    print(texts[main]["weight"].format(name=person.name))
    uindex = userMenu([x[0] for x in weightvalues])
    person.weight = weightvalues[uindex][1]

def hasWeakLungs(main, person):
    person.lungs = "Weak_Lungs"

def getSmoking(main, person):
    uinput = input(texts[main]["smokes"].format(name=person.name))
    person.smoking = uinput.lower() == "yes"
    if not person.smoking:
        person.smoking = None

def getDiseases(main, person):
    diseases = [("Breast Cancer", "Breast_Cancer"), ("Lung Cancer", "Lung_Cancer"),
                ("Prostate Cancer", "Prostate_Cancer"), ("Acute Bronchitis", "Acute_Bronchitis"),
                ("Asthma", "Asthma"), ("COVID-19", "COVID-19"), ("AIDS", "AIDS")]
    uindexes = multiUserMenu([x[0] for x in diseases], textprompt=texts[main]["diseases"].format(name=person.name))
    person.diseases = list([diseases[index][1] for index in uindexes])

def getSymptoms(main, person):
    symptoms = [("Coughing","Coughing"), ("Severe coughing","Heavy_Coughing"),
                ("Minor coughing","Minor_Coughing"),
                ("Severe shortness of breath", "Heavy_Breathlessness"),
                ("Slight shortness of breath", "Minor_Breathlessness"),
                ("High fever","High_Fever"),
                ("Moderate fever","Fever"),
                ("Slight fever","Low_Fever"),
                ("Severe sneezing", "Heavy_Sneezing"),("Slight sneezing","Minor_Sneezing"),
                ("Severe throat pain","Heavy_Throat_Pain"), ("Minor throat pain","Minor_Throat_Pain"),
                ("Severe muscle aching","Heavy_Muscle_Ache"), ("Slight muscle aching","Minor_Muscle_Ache")]
    uindexes = multiUserMenu([x[0] for x in symptoms], textprompt=texts[main]["symptoms"].format(name=person.name))
    person.symptoms = list([symptoms[index][1] for index in uindexes])

healthparams = [("Age", getAge), ("Gender", getGender), ("Took a COVID test", covidTest), ("Weight", getWeight), ("Have/has weak lungs", hasWeakLungs), ("Smoking", getSmoking), ("Have/has an important disease", getDiseases), ("Experience/s illness symptoms", getSymptoms)]

healthliveswith = [("Age", getAge), ("Took a COVID test", covidTest),
                    ("Have/has an important disease", getDiseases)]

healthcompanions = [("Took a COVID test", covidTest), ("Experiences illness symptoms", getSymptoms)]


class AGPerson:

    def __init__(self, name, onto):
        self.name = name
        self.onto = onto
        self.useronto = None
        self.userclass = self.onto.search_one(iri="*User")
        self.age = None
        self.gender = None
        self.lungs = None
        self.smoking = None
        self.weight = None
        self.covidtest = None
        self.diseases = None
        self.symptoms = None
        self.travelvia = None
        self.trans = None
        self.pastTransps = []
        self.gears = []

    def updateTransps(self):
        if (self.trans is not None) and (self.trans.toOnto() is not None):
            self.useronto.isTravellingVia = []
            self.useronto.isTravellingVia.append(self.trans.toOnto())

        self.useronto.hasTravelledVia = []
        for element in self.pastTransps:
            if element.toOnto() is not None:
                self.useronto.hasTravelledVia.append(element.toOnto())

    def toOnto(self):
        if self.useronto is not None:
            return self.useronto
        self.useronto = self.userclass(self.name, namespace=self.onto)
        elements = [self.age, self.gender, self.lungs, self.smoking, self.weight, self.covidtest]
        for element in elements:
            if element is None:
                continue
            ontoel = self.onto.search_one(iri="*" + element)
            self.useronto.hasHealth.append(ontoel)
        if self.diseases is not None:
            for disease in self.diseases:
                ontoel = self.onto.search_one(iri="*" + disease)
                self.useronto.hasHealth.append(ontoel)
        if self.symptoms is not None:
            for symptom in self.symptoms:
                ontoel = self.onto.search_one(iri="*" + symptom)
                self.useronto.hasHealth.append(ontoel)
        

    def linkLivesWith(self, people):
        for person in people:
            person.toOnto()
            self.useronto.livesWith.append(person.toOnto())

    def updateGears(self):
        for gear in self.gears:
            self.useronto.hasProtectiveGear.append(gear)

def extractPerson(main=False, onto=None, functType=None, name=None, time="present"):

    if onto is None:
        raise Exception("Parameters found None")

    if main and functType is None:
        usernametext = "Alright! Tell me about yourself. What is your name?: "
        healthparamsaux = healthparams
    elif functType == "liveswith":
        usernametext = texts[main]["liveswithintroduce"].format(name=name)
        healthparamsaux = healthliveswith
        main = False
    elif functType == "companions":
        usernametext = texts[main]["companionsintroduce"]
        healthparamsaux = healthcompanions
        main = False
    else:
        pass#debug

    username = input(usernametext)
    person = AGPerson(username, onto)
    if username in ag.globalAgent().people:
        name = renameUser(username, ag.globalAgent().people.keys())
        if name is None:
            return ag.globalAgent().people[name]
        person.name = name
    ag.globalAgent().addPerson(person)

    if main:
        userparamstext = "What else could be of interest about you? This data will help me give you a better analysis."
    else:
        userparamstext = "What else could be of interest about " + username + "? This data will help me give you a better analysis."
    
    while(True):
        clear()
        print(userparamstext)

        uindex = userMenu(list(x[0] for x in healthparamsaux)+["That's enough data."])
        if uindex == len(healthparamsaux):
            break
        else:
            clear()
            healthparamsaux[uindex][1](main, person)
            if uindex == len(healthparamsaux)-1:
                healthparamsaux = healthparamsaux[:uindex]
            elif uindex == 0:
                healthparamsaux = healthparamsaux[uindex+1:]
            else:
                healthparamsaux = healthparamsaux[:uindex] + healthparamsaux[uindex+1:]

    if functType != "liveswith":
        liveswith = extractLivingwith(main=main, person=person, onto=onto)
        person.toOnto()
        if liveswith is not None:
            person.linkLivesWith(liveswith)
        gears = extractProtectionGear(main=main, onto=onto, personname=person.name, placename=name)
        if gears is not None:
            person.gears = gears
        person.updateGears()

    clear()
    while(True):
        resp = input(texts[main]["pastactivityyesno"].format(name=person.name))
        if resp.lower() == "no":
            break
        elif resp.lower() == "yes":
            clear()
            pastActivities = AC.extractActivity(main=main, entranceText=texts[main]["pastactivitytell"].format(name=person.name), onto=onto, locations=["Bookshop", "Boutique", "Cafe", "Library", "Restaurant", "Shop", "Stadium"], time="past", agent=person)
            clear()
        else:
            clear()
            print("Please introduce yes or no.")

    person.toOnto()
    return person

def renameUser(username, names):
    resp = input("Mmm... Is this person the same " + username + " you mentioned before? (yes/no): ")
    while(True):
        if resp.lower() == "yes":
            return None
        elif resp.lower() == "no":
            break
        resp = input("Please answer yes or no: ")
    clear()
    print("I see, in that case, we're gonna have to name them something different. What do you want to name this new " + username + "?: ")
    resp = input("Answer: ")
    while(resp in names):
        clear()
        print("You already told me about someone named!")
        resp = input("What do you want to name this new " + username + "?: ")
    return resp

def extractLivingwith(main=False, onto=None, person=None):
    clear()
    liveswith = []
    while(True):
        resp = input(texts[main]["liveswith"].format(name=person.name))
        if resp.lower() == "yes":
            break
        elif resp.lower() == "no":
            return None
        else:
            print("Please answer yes or no")

    while(True):
        clear()
        p = extractPerson(main=main, onto=onto, functType="liveswith", name=person.name)
        liveswith.append(p)
        while(True):
            clear()
            resp = input(texts[main]["furtherliveswith"].format(name=person.name))
            if resp.lower() == "yes":
                break
            elif resp.lower() == "no":
                return liveswith
            else:
                print("Please answer yes or no")
