
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
            if len(set(acceptingStates).intersection(states)):
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

        if 'eps' in self.alphabet:
            epsilon_closures = {}
            for state in self.transitions:
                epsilon_closures[state] = self.epsilon_closure(state)
            print("Epsilon Closures:",epsilon_closures)
            # {'q0': {'0': ['q0'], '1': [], '2': [], 'eps': ['q1']},
            #  'q1': {'0': [], '1': ['q1'], '2': [], 'eps': ['q2']},
            #  'q2': {'0': [], '1': [], '2': ['q2'], 'eps': []}}
            states = []
            states_closures = []
            ts = {}
            newAlphabet = self.alphabet
            newAlphabet.remove('eps')
            i=0
            states_closures.append(list(epsilon_closures.values())[0])
            j = len(states_closures)
            newAcceptingStates = []
            # Epsilon Closures: {'q0': {'q0', 'q1', 'q2'}, 'q1': {'q1'}, 'q2': {'q2'}, 'q3': {'q3'}, 'q4': {'q4'}}
            # states_closures: [{'q0', 'q1', 'q2'}, {'q3'}, set(), {'q4'}]

            # {'q0': {'0': 'q1', '1': 'q1'},
            # 'q1': {'0': 'q2', '1': 'q3'},
            # 'q2': {'0': 'q2', '1': 'q2'},
            # 'q3': {'0': 'q2', '1': 'q3'}}

            # {'q0': {'0': [], '1': [], 'eps': ['q1', 'q2']},
            # 'q1': {'0': ['q3'], '1': [], 'eps': []},
            # 'q2': {'0': [], '1': ['q3'], 'eps': []},
            # 'q3': {'0': [], '1': ['q4'], 'eps': []},
            # 'q4': {'0': [], '1': [], 'eps': []}}
            while j>0:
                
                closures = states_closures[i]
                
                l = list(closures)
                if len(set(self.acceptingStates).intersection(l)):
                    newAcceptingStates.append('q'+str(i))
                ts['q'+str(i)] = {}
                states.append('q'+str(i))
                print('q'+str(i))
                print(closures)
                
                
                for alpha in newAlphabet:
                    nextState = set()
                    for st in l:
                        nextState |= set(self.transitions[st][alpha])
                    ep = set()
                    for n in nextState:
                        if len(n)>0:
                            ep |= epsilon_closures[n]
                    print(alpha,ep)

                    if not(ep in states_closures) and len(ep)>0:
                        states_closures.append(ep)
                        j+=1
                        
                    if len(ep)>0:
                        ts['q'+str(i)][alpha] = 'q'+str(states_closures.index(ep))
                    else:
                        ts['q'+str(i)][alpha] = []

                
                print(ts)
                j-=1
                i+=1 

            print("states_closures:",states_closures)
            print(newAcceptingStates)
            return FA(states,newAlphabet,self.startState,newAcceptingStates,ts)

        else:

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
    
    def epsilon_closure(self,state):
        closure = set([state])
        for next_state in self.transitions[state]['eps']:
            if next_state not in closure:
                closure |= self.epsilon_closure(next_state)

        return closure


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
