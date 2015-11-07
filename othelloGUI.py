#Tyler Robertson
#ID: 22991994

import collections
import gameBoard
import coordinate
import tkinter
import tkinter.messagebox

class othelloGUI :

    def __init__(self, gameInfo : 'gameTypeTuple') :
        self._gameInfo = gameInfo

        #first player to play move
        if gameInfo.whoFirst.upper() == "BLACK" :
            self._playerToken = "black"
        else :
            self._playerToken = "white"

        #get board size from user input
        strSize = gameInfo.boardSize.split(' ')
        self._gameRows = int(strSize[0])
        self._gameCols = int(strSize[1])

        #create two dimensional list of board coordinates
        self._boxLocations = []
        for rows in range(self._gameRows) :
            self._boxLocations.append([" "] * self._gameCols)

        #root window
        self._root_window = tkinter.Tk()
        self._root_window.wm_title("OTHELLO")

        self._canvas = tkinter.Canvas(
            master = self._root_window, width = 500, height = 450)
        self._canvas.grid(
            row = 0, column = 0, padx = 10, pady = 10,
            sticky = tkinter.N + tkinter.S + tkinter.E + tkinter.W)

        #othello textbox that displays info to user
        self._othelloText = tkinter.Text(master = self._root_window, width = 50, height = 25)
        self._othelloText.grid(row = 0, column = 1, padx = 10, pady = 10,
                               sticky = tkinter.N + tkinter.S + tkinter.E + tkinter.W)

        #display directions button
        self._directionsButton = tkinter.Button(self._root_window, text="Display Directions",
                                      width=2, height = 2, command=self._displayDirections)
        self._directionsButton.grid(row = 1, column = 0, padx = 10, pady = 10,
                          sticky = tkinter.N + tkinter.S + tkinter.E + tkinter.W)

        #quit game button
        self._quitButton = tkinter.Button(self._root_window, text="Quit Game",
                                          width = 2, height = 2, command = self._quitButtonAction)
        self._quitButton.grid(row = 1, column = 1, padx = 10, pady = 10,
                              sticky = tkinter.N + tkinter.S + tkinter.E + tkinter.W)

        self._canvas.bind('<Configure>', self._on_canvas_resized)
        self._canvas.bind('<Button-1>', self._on_canvas_clicked)

        self._root_window.rowconfigure(0, weight = 1)
        self._root_window.columnconfigure(0, weight = 1)
        self._root_window.columnconfigure(1, weight = 1)

        #initialize gamestate properties
        self._root_window.focus_force()
        self._gameState = gameBoard.gameState(self._gameRows, self._gameCols, gameInfo)
        self._gameState._setupGameboard()
        self.printToGUI("OTHELLO FEEDBACK...\n\n")

    #draw the gameboard, can be used in an event
    def _drawBoard(self) -> None :
        topX = .1
        topY = .1
        bottomX = .2
        bottomY = .2
        rowCount = 0
        colCount = 0

        self._canvas.delete(tkinter.ALL)

        #current size of the canvas to draw board on
        canvasHeight = self._canvas.winfo_height()
        canvasWidth = self._canvas.winfo_width()

        #draw the gameboard square by square
        for rows in range(self._gameRows):
            colCount = 0
            topX = .1
            bottomX = .2

            for cols in range(self._gameCols):
                topCorner = coordinate.Coordinate(frac = (topX, topY), absolute = None, absolute_size = None)
                bottomCorner = coordinate.Coordinate(frac = (bottomX, bottomY), absolute = None, absolute_size = None)
                absTopX, absTopY = topCorner.absolute((canvasWidth, canvasHeight))
                absBottomX, absBottomY = bottomCorner.absolute((canvasWidth, canvasHeight))

                self._canvas.create_rectangle(absTopX, absTopY, absBottomX, absBottomY, outline = "black", fill = '#008A00')
                self._boxLocations[rowCount][colCount] = [absTopX, absTopY, absBottomX, absBottomY]

                #they there isnt an empty space fill it with the appropriate game piece
                if not self._gameState._board[rows][cols] == ' ' :
                    self._canvas.create_oval(absTopX, absTopY, absBottomX, absBottomY, 
                                             fill = self._gameState._board[rows][cols])

                topX += .1
                bottomX += .1
                colCount += 1

            topY += .1
            bottomY += .1
            rowCount += 1

    def _findSpaceForClick(self, event : tkinter.Event) -> "int, int" :
        #go through box locations to check if user clicked within one of them
        for rows in range(self._gameRows) :
            for cols in range(self._gameCols):

                boxLocation = self._boxLocations[rows][cols]
                isInSpace = (event.x > boxLocation[0] and event.x < boxLocation[2]) and (event.y > boxLocation[1] and event.y < boxLocation[3])

                if isInSpace :
                    return [rows + 1, cols + 1]

    def switchPlayer(self) -> None :

        if self._playerToken == "black" :
            self._playerToken = "white"
        else :
            self._playerToken = "black"

    #print to gui text box, can specify whether to delete all thats in the textbox
    # before printing
    def printToGUI(self, text : str, deleteScreen = False) -> None :

        if deleteScreen :
            self._othelloText.delete(1.0, tkinter.END)

        self._othelloText.insert(tkinter.END, text)

    def printScore(self) -> None :
        numBlack, numWhite = self._gameState._countPieces()
        self.printToGUI("\nSCORE... \nBLACK: {} \n".format(numBlack))
        self.printToGUI("WHITE: {} \n\n".format(numWhite)) 

    def printWinner(self) -> None :
        numBlack, numWhite = self._gameState._countPieces()
        scoreString = "\n\nSCORE:\nBlack : {} \n White : {}".format(numBlack, numWhite)

        if self._gameInfo.winningCondition.upper() == "MOST" :
            if numBlack > numWhite :
                winOutcome = 'BLACK WINS!' + scoreString
            elif numWhite > numBlack :
                winOutcome = 'WHITE WINS!' + scoreString
            else :
                winOutcome = 'TIE GAME!' + scoreString
        else :
            if numWhite < numBlack :
                winOutcome = 'WHITE WINS!' + scoreString
            elif numBlack < numWhite :
                winOutcome = 'BLACK WINS!' + scoreString
            else :
                winOutcome = 'TIE GAME!' + scoreString

        tkinter.messagebox.showinfo("Game Over", winOutcome + "\n\nPress OK to quit")
        self._root_window.destroy()

    def _on_canvas_resized(self, event : tkinter.Event) -> None :
        self._drawBoard()

    def _displayDirections(self) -> None :
        directionsString = """OTHELLO RULES \n\n
        To make a move you have to be sure that you will flip at least one opponent piece \n
        To flip an opponent piece your pieces have to be on either side of a row of opponent pieces\n
        A player will be skipped if no moves are available
        The game continues until both players dont have a move or the board is full"""
        
        tkinter.messagebox.showinfo("Game Directions", directionsString)

    #check if there are moves for either player, will skip player if no moves
    # and will also end game if there are no moves
    def _checkIfMoves(self) -> None :

        if self._playerToken == "white" :
            if not self._gameState._checkIfPossibleMove("white") :
                if not self._gameState._checkIfPossibleMove("black") :
                    self._drawBoard()
                    self.printWinner()

                self.printToGUI("There is no move for white player\nMove again black player\n", True)
                self.switchPlayer()
        else :
            if not self._gameState._checkIfPossibleMove("black") :
                if not self._gameState._checkIfPossibleMove("white"):
                    self._drawBoard()
                    self.printWinner()

                self.printToGUI("There is no move for black player\nMove again white player\n", True)
                self.switchPlayer()

    def _quitButtonAction(self) -> None :
        answer = tkinter.messagebox.askyesno("QUIT GAME","Are You Sure?")

        if answer :
            self._root_window.destroy()

    def _on_canvas_clicked(self, event : tkinter.Event) -> None :

        moveList = self._findSpaceForClick(event)
        #check if the user clicked in a valid space
        if not moveList == None :
            try :
                if self._gameState._makeMove(self._playerToken, moveList[0], moveList[1]):
                    self.switchPlayer()
                    self._drawBoard()

                    if self._gameState._isBoardFull(self._gameInfo) :
                        self._drawBoard()
                        self.printWinner()

                    self.printToGUI("OTHELLO FEEDBACK...\n\n", True)
                    self.printToGUI("{} player's move...\n".format(self._playerToken.upper()))
                    self.printScore()

                else :
                    self.printToGUI("{} player, Please click on a valid space\n".format(self._playerToken))

            except gameBoard.occupiedSpaceException :
                self.printToGUI("{} player, Please click on a space that is unnocupied\n".format(self._playerToken))
            except :
                self.printToGUI("a problem occured, sorry")

        self._checkIfMoves()

    def start(self) -> None:
        self._root_window.mainloop()

#class for getting input from user about the type of othello
# game they would like to play
class getInputGUI :

    def __init__(self) :

        self._master = tkinter.Tk()
        self._master.wm_title("Othello Game Info")

        #entry labels
        self._boardLabel = tkinter.Label(master = self._master, text = 'What size will the board be? Type "rows columns"   ')
        self._whoFirstLabel = tkinter.Label(master = self._master, text = 'Who is going first? Type "black" or "white"   ')
        self._gameTypeLabel = tkinter.Label(master = self._master, text = 'Would you like to start with the traditional setup (white diagonal down) type "yes" or "no"   ')
        self._winLabel = tkinter.Label(master = self._master, text = 'How should the winner be determined? type "most" for most pieces remaining, "least" for least   ')

        #entry spaces
        self._boardEntry = tkinter.Entry(master = self._master, width = 20)
        self._whoFirstEntry = tkinter.Entry(master = self._master, width = 20)
        self._gameTypeEntry = tkinter.Entry(master = self._master, width = 20)
        self._winEntry = tkinter.Entry(master = self._master, width = 20)

        #organize in window
        self._boardLabel.grid(row = 0, column = 0, columnspan = 2, sticky = tkinter.W, padx = 5, pady = 5)
        self._boardEntry.grid(row = 0, column = 1, sticky = tkinter.W + tkinter.E, padx = 5, pady = 5)

        self._whoFirstLabel.grid(row = 1, column = 0, sticky = tkinter.W, padx = 5, pady = 5)
        self._whoFirstEntry.grid(row = 1, column = 1, sticky = tkinter.W + tkinter.E, padx = 5, pady = 5)

        self._gameTypeLabel.grid(row = 2, column = 0, sticky = tkinter.W, padx = 5, pady = 5)
        self._gameTypeEntry.grid(row = 2, column = 1, sticky = tkinter.W + tkinter.E, padx = 5, pady = 5)

        self._winLabel.grid(row = 3, column = 0, sticky = tkinter.W, padx = 5, pady = 5)
        self._winEntry.grid(row = 3, column = 1, sticky = tkinter.W + tkinter.E, padx = 5, pady = 5)

        def buttonAction() -> None :
            #check if the form is filled out before closing
            if self._checkIfFilledOut():
                #retrieve text information
                self._boardSize = self._boardEntry.get()
                self._whoFirst = self._whoFirstEntry.get()
                self._gameType = self._gameTypeEntry.get()
                self._win = self._winEntry.get()

                verifyTuple = checkBoardSize(self._boardSize)
                if not verifyTuple.isValid :
                    tkinter.messagebox.showerror('Invalid Board Size', verifyTuple.errorMessage)
                    return
                self._master.destroy()
            else :
                tkinter.messagebox.showwarning("Othello Info", "Please ensure all blanks are filled in")

        self._master.bind('<Return>', self._on_enter_click)
        self._button = tkinter.Button(self._master, text="Input (or press enter after typing input)"
                                      , width=50, height = 2, command=buttonAction)
        self._button.grid(row = 4, column = 1, sticky = tkinter.E + tkinter.S, padx = 10, pady = 10)

        self._boardEntry.focus_set()
        self._master.mainloop()

    #check to make sure all boxes are filled out in form
    def _checkIfFilledOut(self) -> bool:
        allEntries = [self._boardEntry, self._whoFirstEntry, self._gameTypeEntry, self._winEntry]

        for entry in allEntries :
            if len(entry.get()) == 0:
                return False
        return True 

    #get answers the user specified in the form
    def _retrieveAnswers(self) -> "str[]":
        return [self._boardSize, self._whoFirst, self._gameType, self._win]

    def _on_enter_click(self, event : tkinter.Event) :
        self._button.invoke()

def getGameType() -> 'str[]':

    gameTypeTuple = collections.namedtuple('gameTypeTuple', 'boardSize, whoFirst, isTradSetup, winningCondition')

    gui = getInputGUI()
    gameAnswers = gui._retrieveAnswers()
    
    return gameTypeTuple(gameAnswers[0], gameAnswers[1], gameAnswers[2], gameAnswers[3])

def checkBoardSize(strSize : str) -> 'verifyTuple' :
    verifyTuple = collections.namedtuple('verifyTuple', 'isValid, errorMessage')
    sizeList = strSize.split(' ')

    if len(sizeList) == 2 :
        try :
            intRows = int(sizeList[0])
            intCols = int(sizeList[1])
        except ValueError :
            return verifyTuple(False, 'Please enter a valid integer for your board rows/columns')
        if intRows < 4 or intRows > 16 :
            return verifyTuple(False, 'Your row value is must be 4-16')
        elif not intRows % 2 == 0 :
            return verifyTuple(False, 'You need to enter an even number for the rows')
        elif intCols < 4 or intCols > 16 :
            return verifyTuple(False, 'Your column value must be 4-16')
        elif not intCols % 2 == 0 :
            return verifyTuple(False, 'You need to enter an even number for the columns')

        return verifyTuple(True, None)

    else :
        return verifyTuple(False, 'You need to enter a row and a column in the format "rows columns"')


if __name__ == '__main__' :
    try :
        gameInfo = getGameType()
        othelloGUI(gameInfo).start()
    except AttributeError :
        tkinter.messagebox.showerror('INPUT ERROR', 
                                     'To play othello you need to enter the input properly, run program again')
    except :
        pass
