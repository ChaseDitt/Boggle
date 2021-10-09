# CS1210: HW3 version 1
######################################################################
# Complete the signed() function, certifying that:
#  1) the code below is entirely your own work, and
#  2) it has not been shared with anyone outside the intructional team.
#
def signed():
    return(["cjdittmer"])

######################################################################
# In this homework, you will build the internals for Boggle, a popular
# word game played with 16 6-sided dice. At the same time, in class we
# will develop the interactive user interface for Boggle, so that your
# solution, augmented with what we do in class, will give you a
# playable Boggle game. This assignment will also give us a chance to
# work on a system using the object-oriented paradigm.
#
# This is version 1 of the template file, which does not include the
# user interface.  I will periodically release updated versions, which
# you can then merge into your own code: still, be sure to follow the
# instructions carefully, so as to ensure your code will work with the
# new template versions that contain the GUI we develop in class.
#
# The rules of Boggle are available online. Basically, you will roll
# the dice and arrange them into a 4x4 grid. The top faces of the die
# will display letters, and your job is to find words starting
# anywhere in the grid using only adjacent letters (where "adjacent"
# means vertically, horizontally, and diagonally adjacent). In our
# version of Boggle, there are no word length constraints beyond those
# implicitly contained in the master word list.
#
# Although other dice configurations are possible, the original Boggle
# dice are (in no particular order):
D = ["aaeegn","abbjoo","achops","affkps","aoottw","cimotu","deilrx","delrvy",
     "distty","eeghnw","eeinsu","ehrtvw","eiosst","elrtty","himnqu","hlnnrz"]

# You will need sample() from the random module to roll the die.
from random import sample

######################################################################
# Boggle is the base class for our system; it is analogous to the
# Othello class in our implementation of that game.  It contains all
# the important data elements for the current puzzle, including:
#    Boggle.board = the current puzzle board
#    Boggle.words = the master word list
#    Boggle.solns = the words found in the current puzzle board
#    Boggle.lpfxs = the legal prefixes found in the current puzzle board
# Additional data elements are used for the GUI and scoring, which
# will be added in subsequent versions of the template file.
#
# Note: we will opt to use Knuth's 5,757 element 5-letter word list
# ('words.dat') from the Wordnet puzzle, but the 113,809 element list
# of words from HW1 ('words.txt') should also work just as easily.
#
class Boggle ():
    # This is the class constructor. It should read in the specified
    # file containing the dictionary of legal words and then invoke
    # the play() method, which manages the game.
    def __init__(self, input='words.dat'):

        # Intialize all class variables
        self.board = []
        self.wordList =  []
        self.wordsRead = 0
        self.input = input
        self.solns = []
        self.wordsFound = []
        self.possibleWords = []
        self.lpfxs = []
        self.boardCharactors = []
        pass

    # Printed representation of the Boggle object is used to provide a
    # view of the board in a 4x4 row/column arrangement.
    def __repr__(self):
        for x in self.board:
            print(''.join([str(item)+ ' ' for item in x]))
        return('it ran lol')
        

    # The readwords() method opens the file specified by filename,
    # reads in the word list converting words to lower case and
    # stripping any excess whitespace, and stores them in the
    # Boggle.words list.
    def readwords(self, filename):
        readFile = open(self.input)
        wordList = []
        wordsRead = 0
        for x in readFile:  #Loop to get words for game
            wordList.append(x.strip())
            wordsRead = wordsRead + 1   #counter to show how many words in game
        #set class variables to function variables
        self.wordList = wordList
        self.wordsRead = wordsRead  
        return(self.wordList)
        

    # The newgame() method creates a new Boggle puzzle by rolling the
    # dice and assorting them to the 4x4 game board. After the puzzle
    # is stashed in Boggle.board, the method also computes the set of
    # legal feasible word prefixes and stores this in Boggle.lpfxs.
    def newgame(self):
        board = [[],[],[],[]]
        D1 = sample(D, len(D))
        for x in range(16):
            board[x%4].append(sample(D1[x],1)[0])
        self.board = board
        charList = [item for l in board for item in l]
        self.boardCharactors = (''.join(charList))
        return(self.board)
        

    # The solve() method constructs the list of words that are legally
    # embedded in the given Boggle puzzle. The general idea is search
    # recursively starting from each of the 16 puzzle positions,
    # accumulating solutions found into a list which is then stored on
    # Boggle.solns.
    #
    # The method makes use of two internal "helper" functions,
    # adjacencies() and extend(), which perform much of the work.
    def solve(self):
        self.solns = []
        # Helper function adjacencies() returns all legal adjacent
        # board locations for a given location loc. A board location
        # is considered legal and adjacent if (i) it meets board size
        # constraints (ii) is not contained in the path so far, and
        # (iii) is adjacent to the specified location loc.
        def adjacencies(loc, path):
            adjacentList = []
            row, col = loc
            for x in [-1, 0, 1]:
                for y in [-1, 0, 1]:
                    new_row = row + x
                    new_col = col + y
                    if 0 <= new_row < 4 and 0 <= new_col < 4 and not (x == y == 0):
                        adjacentList.append((new_row, new_col))
            return(adjacentList)

        possibleWords = []
        for x in self.wordList:
            if any(( c not in self.boardCharactors) for c in x):
                pass
            else:
                possibleWords.append(x)
        self.possibleWords = possibleWords

        solute = []
        for x in possibleWords:
            for y in range(1, len(x)):
                if x[0:y] not in solute:
                    solute.append(x[0:y])

        self.lpfxs = solute
        
        
        # Helper function extend() is a recursive function that takes
        # a location loc and a path traversed so far (exclusive of the
        # current location loc). Together, path and loc specify a word
        # or word prefix. If the word is in Boggle.words, add it to
        # Boggle.solns, because it can be constructed within the
        # current puzzle. Otherwise, if the curren prefix is still in
        # Boggle.lpfxs, attempt to extend the current path to all
        # adjacencies of location loc. To do this efficiently, a
        # particular path extension is abandoned if the current prefix
        # is no longer contained in self.lpfxs, because that means
        # there is no feasible solution to this puzzle reachable via
        # this extension to the current path/prefix.
        def extend(loc, path=[]):
            adjacents = adjacencies(loc, [])
            for x in adjacents:
                test = []
                for i in path:
                    test.append(i)
                if x not in test:
                    test.append(x)
                if x not in path:
                    if self.extract(test) in self.possibleWords:
                        if self.extract(test) not in self.solns:
                            self.solns.append(self.extract(test))
                            extend(x, test)
                    elif self.extract(test) in self.lpfxs:
                        extend(x, test)

        for x in range(4):
            for y in range(4):
                extend((x,y), [])


    # The extract() method takes a path and returns the underlying
    # word from the puzzle board.
    def extract(self, path):
        valueList = []
        for x in path:
            valueList.append(self.board[x[0]][x[1]])
        return(''.join(valueList))

    # The checkpath() method takes a path and returns the word it
    # represents if the path is legal (i.e., formed of distinct and
    # sequentially adjacent locations) and realizes a legal word,
    # False otherwise.
    def checkpath(self, path):
        valueList = []
        for x in path:
            valueList.append(self.board[x[0]][x[1]])
        checkWord = (''.join(valueList))
        if checkWord in self.wordList:
            return(checkWord)
        else:
            return(False)
    
    # The round() method plays a round (i.e., a single puzzle) of
    # Boggle. It should return True as long as the player is willing
    # to continue playing additional rounds of Boggle; when it returns
    # False, the Boggle game is over.
    #
    # Hint: Look to HW1's round() function for inspiration.
    #
    # This method will be replaced by an interactive version.
    def round(self):

        #adjacencies brought from solve() to check if user input is adjacent
        def adjacencies(loc, path):
            adjacentList = []
            row, col = loc
            for x in [-1, 0, 1]:
                for y in [-1, 0, 1]:
                    new_row = row + x
                    new_col = col + y
                    if 0 <= new_row < 4 and 0 <= new_col < 4 and not (x == y == 0):
                        adjacentList.append((new_row, new_col))
            return(adjacentList)
        # The recover() helper function converts a list of integers
        # into a path. Thus '3 2 2 1 1 2 2 3' becomes [(3, 2), (2, 1),
        # (1, 2), (2, 3)].
        def recover(path):
            workString = path.replace(" ", "")
            convertList = [ [] for _ in range(int(len(workString)/2)) ]
            i  = 0
            counter = 0
            while i <= int(len(workString)/2) - 1:
                convertList[i].append(int(workString[counter]))
                convertList[i].append(int(workString[counter+1]))
                counter = counter + 2
                i = i + 1
            for x in range(len(convertList)):
                convertList[x] = tuple(convertList[x])
            return(convertList)


        #Menu print
        print("Read ", self.wordsRead, " words")
        print("Puzzle contains ", len(self.solns), " legal solutions")
        print("Welcome to Boggle")
        print("Input 'r1 c1 r2 c2...'; '/'=display, ':'=show, '+'=new puzzle; '.'=quit")
        print("    where 'r1 c1 r2 c2...' specifies a path as series of row,col coordinates.")
        repr(self)
        exitCase = 0    #int to break game loop
        while exitCase == 0:
            userInput = input()     #take user input
            testInput = recover(userInput)  #convert user input to tuple list
            testWord = (self.extract(testInput))    #change user input to word

            #Check to see if input is game input
            if testInput != []:
                testCounter = 0     
                for x in range(len(testInput)-1):   #Test to see if user input is adjacent
                    if testInput[x+1] in adjacencies(testInput[x], []):
                        testCounter = testCounter + 1
                if testCounter == (len(testInput)-1):    #Test to see if user input is adjacent using testCounter
                    if testWord in self.solns:     #checks if the word is in the solution list from solve()
                        if testWord not in self.wordsFound:     #tests to see if word has been said before
                            self.wordsFound.append(testWord)
                            print("'" + str(testWord) + "'", "added to list.")
                        else:
                            print("'" + str(testWord) + "'", "word already found")
                    else: 
                        print("unrecognized word", "'" + str(testWord) + "'")
                else:
                    print("Dice Not Adjacent")
            #If it is not game input check for menu input        
            else:
                if userInput == '/':    #redisplays board
                    repr(self) 
                elif userInput == ':':    #words found so far
                    print(len(self.wordsFound), "words found so far")
                    for x in self.wordsFound:
                        print(x)
                elif userInput == '+':      #new puzzle
                    self.newgame()  #create new board
                    self.solve()    #find solutions in new board

                    #Menu print
                    print("Read ", self.wordsRead, " words")
                    print("Puzzle contains ", len(self.solns), " legal solutions")
                    print("Welcome to Boggle")
                    print("Input 'r1 c1 r2 c2...'; '/'=display, ':'=show, '+'=new puzzle; '.'=quit")
                    print("    where 'r1 c1 r2 c2...' specifies a path as series of row,col coordinates.")
                    repr(self)
                    self.wordsFound = []

                elif  userInput == '.':     #ends game
                    print("You found ", len(self.wordsFound), " of ", len(self.solns), 'possible solutions.' )
                    print('Thanks for playing')
                    exitCase = 1    #sets value to break while loop

                #If input doesnt match anything
                else:
                    print("Error bad input")
 
            

    # The play() method when invoked initiates a sequence of
    # individual Boggle rounds by repeatedly invoking the rounds()
    # method as long as the user indicates they are interested in
    # playing additional puzzles.
    #
    # Hint: Look to HW1's play() function for inspiration.
    #
    # This method will be replaced by an interactive version.
    def play(self):
        self.newgame()
        self.readwords(input)
        self.solve()
        self.round()

#B1 = Boggle('words.dat')
B2 = Boggle('words.txt')
B2.play()
'''
B1.newgame()
B1.readwords('words.txt')
print(B1.board)
print(B1.wordList)
print(B1.extract([(2,2),(1,1),(1,0),(0,0)]))
print(B1.checkpath([(2,2),(1,1),(1,0),(0,0)]))
'''


######################################################################
if __name__ == '__main__':
    Boggle()