from queue import Queue
import operator
from solver import *
import copy

class SolverDFS(UninformedSolver):
    def __init__(self, gameMaster, victoryCondition):
        super().__init__(gameMaster, victoryCondition)


    def solveOneStep(self):
        """
        Go to the next state that has not been explored. If a
        game state leads to more than one unexplored game states,
        explore in the order implied by the GameMaster.getMovables()
        function.
        If all game states reachable from a parent state has been explored,
        the next explored state should conform to the specifications of
        the Depth-First Search algorithm.

        Returns:
            True if the desired solution state is reached, False otherwise
        """
        ### Student code goes here



        currentstate = self.currentState
        moves = self.gm.getMovables()
        children = self.gm.getMovables()
        '''
        print ("CURRENTSTATE" + str(self.currentState.state))
        print ("MOVABLES:")
        if moves:
            for m in moves:
                print (str(m))
        print ("CHILDINDEX:")
        print (currentstate.nextChildToVisit)
        print ("*********")
        '''


        if self.currentState.state == self.victoryCondition:
            return True

        else:
            self.visited[self.currentState] = True

            if children == []:
                # print("no moves to take")
                self.gm.reverseMove(self.currentState.requiredMovable)
                self.currentState = self.currentState.parent
                self.currentState.state = self.gm.getGameState()

            else:
                while currentstate.nextChildToVisit < len(children):
                    newmove = children[currentstate.nextChildToVisit]
                    currentstate.nextChildToVisit += 1
                    cur = self.gm.getGameState()
                    self.gm.makeMove(newmove)
                    newstate = GameState(self.gm.getGameState(), currentstate.depth + 1, newmove)
                    if self.visited.__contains__(newstate):
                        backmove = newstate.requiredMovable
                        self.gm.reverseMove(backmove)
                        continue
                    # self.gm.makeMove(newmove.requiredMovable)
                    self.visited[newstate] = False
                    newstate.parent = currentstate
                    self.currentState.children.append(newstate)
                    self.currentState = newstate
                    #  self.generate_children()
                    return
                if currentstate.parent:
                    backmove = currentstate.requiredMovable
                    self.gm.reverseMove(backmove)
                    self.currentState = currentstate.parent
                    return




            '''
            else:
                for newmove in children:
                    self.gm.makeMove(newmove)
                    newstate = GameState(self.gm.getGameState(), currentstate.depth+1, newmove)
                    # print("move to new state")
                    if self.visited.__contains__(newstate):
                        # print("visited")
                        self.gm.reverseMove(newmove)
                        self.currentState.depth -= 1
                        self.currentState.nextChildToVisit += 1

                    else:
                        # print("expand")
                        newstate.parent = currentstate
                        self.currentState.children.append(newstate)
                        self.currentState = newstate
                        return
            '''





class SolverBFS(UninformedSolver):
    def __init__(self, gameMaster, victoryCondition):
        super().__init__(gameMaster, victoryCondition)
        self.q = Queue()
        self.path = dict()
        self.rootnode = []

    def solveOneStep(self):
        """
        Go to the next state that has not been explored. If a
        game state leads to more than one unexplored game states,
        explore in the order implied by the GameMaster.getMovables()
        function.
        If all game states reachable from a parent state has been explored,
        the next explored state should conform to the specifications of
        the Breadth-First Search algorithm.

        Returns:
            True if the desired solution state is reached, False otherwise
        """
        ### Student code goes here

        # print("CURRENTSTATE" + str(self.currentState.state))
        currentstate = self.currentState
        if self.currentState.state == self.victoryCondition:
            return True
        if not self.currentState.parent:
            self.path[currentstate] = []
            self.rootnode = self.gm.getGameState()
        else:
            self.visited[self.currentState] = True
        # put non-visited children in queue
        children = self.gm.getMovables()
        for c in children:
            if str(c.terms[0]) == 'empty':
                children.remove(c)
        for newmove in children:
            self.gm.makeMove(newmove)
            newstate = GameState(self.gm.getGameState(), currentstate.depth + 1, newmove)
            if self.visited.__contains__(newstate):
                self.gm.reverseMove(newmove)
            else:
                self.q.put(newstate)
                self.visited[newstate] = True
                newstate.parent = currentstate
                self.path[newstate] = self.path[currentstate].copy()
                self.path[newstate].append(newstate)
                self.gm.reverseMove(newmove)

        # go back to root node
        current = self.currentState
        gs = self.gm.getGameState()
        flag = operator.eq(gs, self.rootnode)
        pathtoroot = self.path[currentstate]
        pathtoroot.reverse()
        if not flag:
            for state in pathtoroot:
                backmove = state.requiredMovable
                self.gm.reverseMove(backmove)
                gs = self.gm.getGameState()

        # current = GameState(self.gm.getGameState(), current.depth - 1, backmove)

        # go to next node
        self.currentState = self.q.get()
        pathToNext = self.path[self.currentState]
        for p in pathToNext:
            move = p.requiredMovable
            self.gm.makeMove(move)

        '''
        if self.currentState.state == self.victoryCondition:
            return True

        if self.currentState.depth == 0:
            self.path[self.currentState] = []

            # Add all possible moves that can be taken from the given state to the states list of children
        posmoves = self.gm.getMovables()
        curr = self.currentState
        self.visited[curr] = True

        # add children
        if posmoves:
            for move in posmoves:
                self.gm.makeMove(move)
                child_state = GameState(self.gm.getGameState(), curr.depth + 1, move)
                if child_state not in self.visited:
                    self.visited[child_state] = True
                    self.Q.put(child_state)
                    self.path[child_state] = self.path[curr].copy()
                    self.path[child_state].append(child_state)
                self.gm.reverseMove(move)

        path_to_root = self.path[self.currentState]
        path_to_root.reverse()
        self.currentState = self.Q.get()
        path_to_next = self.path[self.currentState]

        for n in path_to_root:
            self.gm.reverseMove(n.requiredMovable)

        for p in path_to_next:
            self.gm.makeMove(p.requiredMovable)
            print(self.gm.getGameState())

        if self.currentState.state == self.victoryCondition:
            return True

        return False
        '''




