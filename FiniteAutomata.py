
class FA():
    def __init__(self,states,alphabet,startState,acceptingStates,transitions):
        if type(states) is list:
            self.states = states
        else:
            raise Exception("states variable is not of type list")

        if type(alphabet) is list:
            self.alphabet = alphabet
        else:
            raise Exception("alphabet variable is not of type list")

        if startState in states:
            self.startState = startState
        else:
            raise Exception("Start state is not in all states")
        
        if type(acceptingStates) is list:
            if set(acceptingStates).issubset(states):
                self.acceptingStates = acceptingStates
            else:
                raise Exception("The accepting states set is not a subset of all states")
        else:
            raise Exception("acceptingStates variable is not of type list")
        if type(transitions) is dict:
            self.transitions =transitions
        else:
            raise Exception("transitions variable is not of type dict")
        

    def convert2DFA(self):

        states = [self.states[0]]
        ts = {}
        ts[self.states[0]] = getTransitionsOf(self.states[0],self.transitions)
        i= len(states)
        while i>=0:

            for a, toStates in ts[states[i- len(states)]].items():
                    temp = '-'.join(toStates)
                    
                    if not(temp in states) and temp != '':
                        newTransitions =  getTransitionsOf(temp,self.transitions)
                        states.append(temp)
                        ts[temp] = newTransitions
                        i+=1
 
            i-=1

        ts = self.renameStates(ts)
        acceptingStates = self.getAcceptingStates(self.acceptingStates,states)

        return FA(states,self.alphabet,self.startState,acceptingStates,ts)
    
    def renameStates(self,d):
        for state,stateTransition in d.items():
            for a, s in stateTransition.items():
                d[state][a] = '-'.join(s)

        return d
    
    def getAcceptingStates(self,oldStates,newStates):
        states = []
        for s in newStates:
            if s in oldStates or len(set(oldStates).intersection(set(s.split('-'))))>0:
                states.append(s)
        return states


def unionLists(first_list,second_list):
    return first_list + list(set(second_list) - set(first_list)) 
  
def getTransitionsOf(s,transitions):
    states=s.split('-')
    l={}
    for state, stateTransitions in transitions.items():
        if state in states:
            for i,j in stateTransitions.items():
                if i in l.keys():
                    l[i] = unionLists(l[i],j)
                else:
                    l[i] = j
    return l
