from game_master import GameMaster
from read import *
from util import *

class TowerOfHanoiGame(GameMaster):

    def __init__(self):
        super().__init__()
        
    def produceMovableQuery(self):
        """
        See overridden parent class method for more information.

        Returns:
             A Fact object that could be used to query the currently available moves
        """
        return parse_input('fact: (movable ?disk ?init ?target)')

    def getGameState(self):
        """
        Returns a representation of the game in the current state.
        The output should be a Tuple of three Tuples. Each inner tuple should
        represent a peg, and its content the disks on the peg. Disks
        should be represented by integers, with the smallest disk
        represented by 1, and the second smallest 2, etc.

        Within each inner Tuple, the integers should be sorted in ascending order,
        indicating the smallest disk stacked on top of the larger ones.

        For example, the output should adopt the following format:
        ((1,2,5),(),(3, 4))

        Returns:
            A Tuple of Tuples that represent the game state
        """
        ### student code goes here
        list1 = []
        list2 = []
        list3 = []
        list = ()
        list_of_bindings1 = self.kb.kb_ask(parse_input('fact: on ?disk peg1)'))
        if list_of_bindings1 == False:
            pass
        else:
            for x in list_of_bindings1:
                a = x.bindings[0].constant.element[4]
                list1.append(int(a))
        #print(list1)

        list_of_bindings2 = self.kb.kb_ask(parse_input('fact: on ?disk peg2)'))
        if list_of_bindings2 == False:
            pass
        else:
            for x in list_of_bindings2:
                b = x.bindings[0].constant.element[4]
                list2.append(int(b))
        #print(list2)

        list_of_bindings3 = self.kb.kb_ask(parse_input('fact: on ?disk peg3)'))
        if list_of_bindings3 == False:
            pass
        else:
            for x in list_of_bindings3:
                c = x.bindings[0].constant.element[4]
                list3.append(int(c))
        list1.sort()
        list2.sort()
        list3.sort()

        list = (tuple(list1),tuple(list2),tuple(list3))
        return list



    def makeMove(self, movable_statement):
        """
        Takes a MOVABLE statement and makes the corresponding move. This will
        result in a change of the game state, and therefore requires updating
        the KB in the Game Master.

        The statement should come directly from the result of the MOVABLE query
        issued to the KB, in the following format:
        (movable disk1 peg1 peg3)

        Args:
            movable_statement: A Statement object that contains one of the currently viable moves

        Returns:
            None
        """
        ### Student code goes here
        move = movable_statement.terms

        if str(movable_statement.terms[1]) == 'peg1':
            a = 0
        elif str(movable_statement.terms[1]) == 'peg2':
            a = 1
        else:
            a = 2

        if str(movable_statement.terms[2]) == 'peg1':
            b = 0
        elif str(movable_statement.terms[2]) == 'peg2':
            b = 1
        else:
            b = 2

        oldstate = self.getGameState()
        # retract target peg empty & assert disk top & retract original disk top
        self.kb.kb_retract(parse_input('fact: (empty ' + str(move[2]) + ')'))
        self.kb.kb_assert(parse_input('fact: (top ' + str(move[0]) + ' ' + str(move[2])+')'))
        self.kb.kb_assert(parse_input('fact: (on ' + str(move[0]) + ' ' + str(move[2])+')'))
        self.kb.kb_retract(parse_input('fact: (top ' + str(move[0]) + ' ' + str(move[1]) + ')'))
        self.kb.kb_retract(parse_input('fact: (on ' + str(move[0]) + ' ' + str(move[1]) + ')'))

        # for current peg
        if len(oldstate[a]) == 1:
            self.kb.kb_assert(parse_input('fact: (empty ' + str(move[1]) + ')'))
        else:
            self.kb.kb_assert(parse_input('fact: (top disk' + str(oldstate[a][1]) + ' ' + str(move[1]) + ')'))

        # for target peg
        if oldstate[b] == ():
            pass
        else:
            self.kb.kb_retract(parse_input('fact: top disk' + str(oldstate[b][0]) + ' ' + str(move[2]) + ')'))
        '''
        print("game state")
        currentstate = self.getGameState()
        print(".......")
        print("test make move")
        print(str(currentstate))
        print(".......")
        '''
        return


    def reverseMove(self, movable_statement):
        """
        See overridden parent class method for more information.

        Args:
            movable_statement: A Statement object that contains one of the previously viable moves

        Returns:
            None
        """
        pred = movable_statement.predicate
        sl = movable_statement.terms
        newList = [pred, sl[0], sl[2], sl[1]]
        self.makeMove(Statement(newList))

class Puzzle8Game(GameMaster):

    def __init__(self):
        super().__init__()

    def produceMovableQuery(self):
        """
        Create the Fact object that could be used to query
        the KB of the presently available moves. This function
        is called once per game.

        Returns:
             A Fact object that could be used to query the currently available moves
        """
        return parse_input('fact: (movable ?piece ?initX ?initY ?targetX ?targetY)')

    def getGameState(self):
        """
        Returns a representation of the the game board in the current state.
        The output should be a Tuple of Three Tuples. Each inner tuple should
        represent a row of tiles on the board. Each tile should be represented
        with an integer; the empty space should be represented with -1.

        For example, the output should adopt the following format:
        ((1, 2, 3), (4, 5, 6), (7, 8, -1))

        Returns:
            A Tuple of Tuples that represent the game state
        """
        ### Student code goes here

        list = [[0,0,0],[0,0,0],[0,0,0]]
        list_of_bindings = self.kb.kb_ask(parse_input("fact: (at ?tile ?x ?y"))
        for i in range(0,len(list_of_bindings)):
            tile = list_of_bindings[i]['?tile'][-1]
            x = int(list_of_bindings[i]['?x'][-1])-1
            y = int(list_of_bindings[i]['?y'][-1])-1
            if tile == 'y':
                list[y][x] = -1
            else:
                list[y][x] = int(tile)
        list = (tuple(list[0]),tuple(list[1]),tuple(list[2]))
        return list



    def makeMove(self, movable_statement):
        """
        Takes a MOVABLE statement and makes the corresponding move. This will
        result in a change of the game state, and therefore requires updating
        the KB in the Game Master.

        The statement should come directly from the result of the MOVABLE query
        issued to the KB, in the following format:
        (movable tile3 pos1 pos3 pos2 pos3)

        Args:
            movable_statement: A Statement object that contains one of the currently viable moves

        Returns:
            None
        """
        ### Student code goes here
        # (movable ?tile ?x0 ?y0 ?x ?y)
        # fact: (at ?tile ?x ?y)

        tile = str(movable_statement.terms[0])[-1]
        x0 = str(movable_statement.terms[1])[-1]
        y0 = str(movable_statement.terms[2])[-1]
        x = str(movable_statement.terms[3])[-1]
        y = str(movable_statement.terms[4])[-1]
        oldlocation = parse_input('fact: (at tile' + str(tile) + ' pos' + x0 + ' pos' + y0 + ')' )
        newlocation = parse_input('fact: (at tile' + str(tile) + ' pos' + x + ' pos' + y + ')')
        oldempty = parse_input('fact: (at empty pos' + x + ' pos' + y)
        newempty = parse_input('fact: (at empty pos' + x0 + ' pos' + y0)
        self.kb.kb_retract(oldlocation)
        self.kb.kb_retract(oldempty)
        self.kb.kb_assert(newlocation)
        self.kb.kb_assert(newempty)





    def reverseMove(self, movable_statement):
        """
        See overridden parent class method for more information.

        Args:
            movable_statement: A Statement object that contains one of the previously viable moves

        Returns:
            None
        """
        pred = movable_statement.predicate
        sl = movable_statement.terms
        newList = [pred, sl[0], sl[3], sl[4], sl[1], sl[2]]
        self.makeMove(Statement(newList))
