
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
            # Get all epsilon closure of all states
            for state in self.transitions:
                epsilon_closures[state] = self.epsilon_closure(state)
            print("Epsilon Closures:",epsilon_closures)
            states = []
            states_closures = []
            ts = {}
            newAlphabet = self.alphabet
            newAlphabet.remove('eps')
            i=0
            # Add the epsilon closures of the first state
            states_closures.append(list(epsilon_closures.values())[0])
            j = len(states_closures)
            newAcceptingStates = []

            # Loop on new added states
            while j>0:
                
                closures = states_closures[i]
                
                l = list(closures)
                # If any state in accepting state is in this epsilon closures add it to the accepting states
                if len(set(self.acceptingStates).intersection(l)):
                    newAcceptingStates.append('q'+str(i))
                

                ts['q'+str(i)] = {}
                states.append('q'+str(i))
                print('q'+str(i))
                print(closures)
                
                #  Loop on each alphabet
                for alpha in newAlphabet:
                    nextState = set()
                    # Get all next states based on the input alphabet
                    for st in l:
                        nextState |= set(self.transitions[st][alpha])
                    ep = set()
                    # loop on next states of the alphabet
                    for n in nextState:
                        if len(n)>0:
                            # Get all epsilon closures for each next state
                            ep |= epsilon_closures[n]
                    print(alpha,ep)
                    # If this state epsilon closure in not already added then add it
                    if not(ep in states_closures) and len(ep)>0:
                        states_closures.append(ep)
                        j+=1
                    # To handle when there is no edge between states or when there is no epsilon closures
                    if len(ep)>0:
                        ts['q'+str(i)][alpha] = 'q'+str(states_closures.index(ep))
                    else:
                        ts['q'+str(i)][alpha] = []

                
                print(ts)
                # Decrement j to loop
                j-=1
                # Increment the new states counter
                i+=1 

            print("states_closures:",states_closures)
            print(newAcceptingStates)
            return FA(states,newAlphabet,self.startState,newAcceptingStates,ts)

        else:

            states = [self.states[0]]
            ts = {}
            # Add first state
            ts[self.states[0]] = getTransitionsOf(self.states[0],self.transitions)
            i= len(states)
            # Loop whenever a state is added
            while i>=0:
                # Loop to get (To states) from the transitions dictionary
                for a, toStates in ts[states[i- len(states)]].items():
                        # If the same input alphabet goes to more than one state then name this state with '-' separated between the names of state
                        temp = '-'.join(toStates)
                        # If this state is not already added then add it
                        if not(temp in states) and temp != '':
                            newTransitions =  getTransitionsOf(temp,self.transitions)
                            states.append(temp)
                            ts[temp] = newTransitions
                            i+=1
                i-=1
            # A function to rename states
            ts = self.renameStates(ts)
            # Function to get Accepting states
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
