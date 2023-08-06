import itertools
import json
import io
import copy
import time

class Action:
    def __init__(self, name, pre, eff, intrinsicvalue):
        self.name = name
        self.pre = pre
        self.eff = eff
        self.intrinsicvalue = intrinsicvalue
        
    def __str__(self):
        return self.name
        
class Event:
    def __init__(self, name, pre, eff, times = []):
        self.name = name
        self.pre = pre
        self.eff = eff
        self.times = times
        
class Plan:
    """
    Assumes a plan that successfully reaches its goal.
    """
    def __init__(self, endoPlan):
        self.endoActions = endoPlan
        
    def __str__(self):
        s = "["
        for a in self.endoActions:
            s += str(a) + ","
        return s+"]"

    def __repr__(self):
        return self.__str__()

class Situation:
    def __init__(self, json = None):
        if json == None:
            self.actions = None
            self.events = None
            self.init = None
            self.goal = None
            self.affects = None
            self.utilities = None
        else:
            self.parseJSON(json)

        self.alethicAlternatives = []
        self.epistemicAlternatives = []
        self.creativeAlternatives = []

    def cloneSituation(self):
        return Situation(self.jsonfile)
 
    def parseJSON(self, jsonfile):
        self.jsonfile = jsonfile
        with io.open(jsonfile) as data_file:
            data = json.load(data_file)
            self.actions = []
            for a in data["actions"]:
                action = Action(a["name"], a["preconditions"], a["effects"], a["intrinsicvalue"])
                self.actions += [action]
            self.events = []
            for a in data["events"]:
                event = Event(a["name"], a["preconditions"], a["effects"], a["timepoints"])
                self.events += [event]
            self.affects = data["affects"]
            self.goal = data["goal"]
            self.init = data["initialState"]
            planactions = []
            for a in data["plan"]:
                for b in self.actions:
                    if a == b.name:
                        planactions += [b]
            self.plan = Plan(planactions)
            self.utilities = data["utilities"]
    
    def getHarmfulConsequences(self):
        allCons = self.getAllConsequences()
        harmful = []
        for u in self.utilities:
            if u["utility"] < 0:
                if self.isSatisfied(u["fact"], allCons):
                    harmful += [u["fact"]]  
        return harmful      
    
    def getAllConsequences(self):
        return self.simulate()

    def getUtility(self, fact):
        for u in self.utilities:
            if fact == u["fact"]:
                return u["utility"]
        return 0

    def getFinalUtility(self):
        utility = 0
        sn = self.simulate()
        for k, v in sn.items():
            utility += self.getUtility({k:v})
        return utility
        
    def isInstrumentalAt(self, effect, positions):
        sn = self.simulate(blockEffect = effect, blockPositions = positions)
        return not self.satisfiesGoal(sn)    
        
    def isInstrumental(self, effect):
        for p in self.getSubPlans(len(self.plan.endoActions)):
            if self.isInstrumentalAt(effect, p):
                return True
        return False
        
    def treatsAsEnd(self, p):
        for e in self.affects[p]["neg"]:
            if self.isSatisfied(e, self.goal):
                return False
        for e in self.affects[p]["pos"]:
            if self.isSatisfied(e, self.goal):
                return True
        return False
        
    def treatsAsMeans(self, p):
        for e in self.affects[p]["pos"] + self.affects[p]["neg"]:
            if self.isInstrumental(e):
                return True
        return False
        
    def agentivelyCaused(self, effect):
        sn = self.simulate()
        if not self.isSatisfied(effect, sn):
            return False
        for p in self.getSubPlans():
            sn = self.simulate(p)
            if not self.isSatisfied(effect, sn):
                return True
        return False
        
    def evaluate(self, principle):
        return principle().permissible(self)
   
    def execute(self, action, state, blockEffect = None):
        if blockEffect == None:
            blockEffect = {}
        if self.isApplicable(action, state):
            return self.apply(action, state, blockEffect)
        return state
            
    def isApplicable(self, action, state):
        return self.isSatisfied(action.pre, state)
        
    def apply(self, action, state, blockEffect = None):
        if blockEffect == None:
            blockEffect = {}
        si = copy.deepcopy(state)
        for condeff in action.eff:
            if self.isSatisfied(condeff["condition"], si):
                for v in condeff["effect"].keys():
                    if not v in blockEffect or blockEffect[v] != condeff["effect"][v]:    
                        state[v] = condeff["effect"][v]
        return state
    
    def isSatisfied(self, cond, state):
        for k in cond.keys():
            if k not in state or cond[k] != state[k]:
                return False
        return True
        
    def satisfiesGoal(self, state):
        return self.isSatisfied(self.goal, state)
           
    def latestExo(self):
        m = 0
        for e in self.events:
            if max(e.times) > m:
                m = max(e.times)
        return m
        
    def getSubPlans(self, n = None):       
        if n == None:
            n = len(self.plan.endoActions)
        return itertools.product([0, 1], repeat=n)
 
    def simulate(self, skip = None, blockEffect = None, blockPositions = None):
        """
        param init: The initial State
        param skip: A list of bits representing for each endogeneous action in the plan whether or not to execute it.
        param blockEffect: An effect to counterfactually not been added to a successor state at actions specified in blockPositions.
        param blockPositions: Positions in the plan where the blockEffect should be blocked (given as a list of bits, one for each endogeneous action in the plan).
        """
        init = copy.deepcopy(self.init)
        if skip == None:
            skip = [0]*len(self.plan.endoActions)
        if blockEffect == None:
            blockEffect = {}
        if blockPositions == None:
            blockPositions = [0] * len(self.plan.endoActions)
        cur = init
        for t in range(len(self.plan.endoActions)):
            if not skip[t]:
                if blockPositions[t] == 1:
                    cur = self.execute(self.plan.endoActions[t], cur, blockEffect)
                else:
                    cur = self.execute(self.plan.endoActions[t], cur)
            for e in self.events:
                if t in e.times:
                    cur = self.execute(e, cur)
        if self.latestExo() >= len(self.plan.endoActions):
            for t in range(len(self.plan.endoActions), self.latestExo()+1):        
                for e in self.events:
                    if t in e.times:
                        cur = self.execute(e, cur)
        return cur
    
    def generatePlan(self, frontier = None, k = 10, principle = None):
        """
        A very simple planner.
        """
        if k == 0:
            return False
        if frontier == None:
            frontier = [Plan([])]
            # Maybe the empty plan already does the job
            s = self.planFound(frontier[0], principle)
            if s:
                return s
        for a in self.actions:
            newplancand = Plan(frontier[0].endoActions+[a])
            s = self.planFound(newplancand, principle)
            if s:
                return s
            frontier += [newplancand]
        return self.generatePlan(frontier[1:], k - 1, principle)

    def planFound(self, newplancand, principle):
        newsit = Situation(self.jsonfile)
        newsit.plan = newplancand
        fstate = newsit.simulate()
        if self.satisfiesGoal(fstate):
            if principle == None or principle().permissible(newsit):
                return newsit
        return False    

    def generateCreativeAlternative(self, principle):
        for c in self.creativeAlternatives:
            c.plan = c.generatePlan(principle = principle)
            if c.plan != False:
                return c
        return False

    def makeMoralSuggestion(self, principle):
        # Maybe the situation is alright as is
        if principle().permissible(self):
            return self
        # Maybe just the plan is bad and we can find a better one
        p = self.generatePlan(principle = principle)
        if p != False:
            sit = self.cloneSituation()
            sit.plan = p
            if principle().permissible(sit):
                return sit
        # Otherwise, let's be creative
        return self.generateCreativeAlternative(principle)
        

"""
Ethical Principles
"""

class Deontology:
    def permissible(self, situation):
        for a in situation.plan.endoActions:
            if a.intrinsicvalue == "bad":
                return False
        return True

class DoNoHarm:
    def permissible(self, situation):
        for h in situation.getHarmfulConsequences():
            causes = situation.agentivelyCaused(h)
            if causes:
                return False
        return True

class DoNoInstrumentalHarm:
    def permissible(self, situation):
        for h in situation.getHarmfulConsequences():
            if situation.isInstrumental(h):
                return False
        return True

class KantianHumanity:
    def permissible(self, situation):
        for p in situation.affects.keys():
            if situation.treatsAsMeans(p) and not situation.treatsAsEnd(p):
                return False
        return True

class Utilitarianism:
    def permissible(self, situation):
        u = situation.getFinalUtility()
        for a in situation.alethicAlternatives:
            if a.getFinalUtility() > u:
                return False, u
        return True
        
class DoubleEffectPrinciple:
    def permissible(self, situation):
        # Deontology
        if not Deontology().permissible(situation):
            return False, "deon"
        # No bad goals, one good one
        foundgood = False
        for k,v in situation.goal.items():
            if situation.getUtility({k:v}) < 0:
                return False, "bad goal"
            if situation.getUtility({k:v}) > 0:
                foundgood = True
        if not foundgood:
            return False
        # No bad means
        if not DoNoInstrumentalHarm().permissible(situation):
            return False
        # All in all positive
        return situation.getFinalUtility() > 0

