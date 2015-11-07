#Tyler Robertson
#ID : 22991994

import collections
import copy

BLACK = 'black'
WHITE = 'white'

class invalidMoveException(Exception) :
    '''this will be raised if the user enters
       a move that is out of range of the current board'''
    pass

class occupiedSpaceException(Exception) :
    '''this exception is fired when the player
       tries to move to a space that is already
       occupied by a playing piece'''
    pass


class gameState :

    BLACK = 'black'
    WHITE = 'white'

    def __init__(self, boardRows, boardCols, gameType : 'gameTypeTuple') :

        self._boardRows = boardRows
        self._boardCols = boardCols
        self._gameType = gameType

        self._board = []

        for rows in range(boardRows) :

            self._board.append([" "] * boardCols)

        self._setupGameboard()
            
    def _setupGameboard(self) -> None :

        #determine the middle of the board
        upperDiagonalRow = (self._boardRows // 2) - 1
        upperDiagonalCol = (self._boardCols // 2) - 1

        if self._gameType.isTradSetup.upper() == 'YES' :
            self._board[upperDiagonalRow][upperDiagonalCol] = gameState.WHITE
            self._board[upperDiagonalRow  + 1][upperDiagonalCol + 1] = gameState.WHITE
            self._board[upperDiagonalRow][upperDiagonalCol + 1] = gameState.BLACK
            self._board[upperDiagonalRow + 1][upperDiagonalCol] = gameState.BLACK
            
        else :
            self._board[upperDiagonalRow][upperDiagonalCol] = gameState.BLACK
            self._board[upperDiagonalRow  + 1][upperDiagonalCol + 1] = gameState.BLACK
            self._board[upperDiagonalRow][upperDiagonalCol + 1] = gameState.WHITE
            self._board[upperDiagonalRow + 1][upperDiagonalCol] = gameState.WHITE


    def _makeMove(self, playerToken : str, row : int, col : int) -> bool :

        if row > self._boardRows or row < 1 :
            raise invalidMoveException()
        elif col > self._boardCols or col < 1 :
            raise invalidMoveException()
        elif not self._board[row - 1][col - 1] == " " :
            raise occupiedSpaceException()

        row -= 1
        col -= 1

        self._board[row][col] = playerToken

        isMove = self._checkForFlips(playerToken, row, col)

        if not isMove :
            self._board[row][col] = ' '

        return isMove

    def _checkForFlips(self, playerToken : str, row : int, col : int) -> bool :

        isHorizontal = self._checkHorizontal(row, col, playerToken)

        isVerticle = self._checkVerticle(row, col, playerToken)

        isUpDiagonal = self._checkUpDiagonal(row, col, playerToken)

        isDownDiagonal = self._checkDownDiagonal(row, col, playerToken)
        
        if isHorizontal or isVerticle or isUpDiagonal or isDownDiagonal :
            return True
        else :
            return False
        

    def _checkHorizontal(self, row : int, col : int, playerToken : str) -> bool :
        playerCol = col

        if playerToken == gameState.BLACK :
            opponentToken = gameState.WHITE
        else :
            opponentToken = gameState.BLACK

        #loop through the row in question
        for colIndex in range(self._boardCols) :

            flip = True
            foundTwo = False
            startCol = 0
            endCol = 0

            #find first piece
            if self._board[row][colIndex] == playerToken :
                startCol = colIndex

                #check for another piece
                for col in range(colIndex + 1, self._boardCols) :

                    if self._board[row][col] == playerToken :
                        foundTwo = True
                        endCol = col
                        break

                if foundTwo :
                    #check if all spaces between are opponents color
                    for checkCol in range(startCol + 1, endCol) :

                        if not self._board[row][checkCol] == opponentToken :
                            flip = False
                            break

            if foundTwo and flip and not startCol + 1 == endCol :
                if playerCol == startCol or playerCol == endCol :
                    for flipCol in range(startCol + 1, endCol) :
                        self._board[row][flipCol] = playerToken
                    return True

        return False
    

    def _checkVerticle(self, row: int, col : int,  playerToken : str) -> bool :
        playerRow = row

        if playerToken == gameState.BLACK :
            opponentToken = gameState.WHITE
        else :
            opponentToken = gameState.BLACK

        #loop through the column last move played in
        for rowIndex in range(self._boardRows):

            flip = True
            foundTwo = False
            startRow = 0
            endRow = 0

            #find the first piece
            if self._board[rowIndex][col] == playerToken :
                startRow = rowIndex

                #check for another piece
                for row in range(rowIndex + 1, self._boardRows) :

                    if self._board[row][col] == playerToken :
                        foundTwo = True
                        endRow = row
                        break

                if foundTwo :
                    #check if all spaces between are opponent color
                    for checkRow in range(startRow + 1, endRow) :

                        if not self._board[checkRow][col] == opponentToken :
                            flip = False
                            break
                    
            if foundTwo and flip and not startRow + 1 == endRow :

                if playerRow == startRow or playerRow == endRow :
                    for flipRow in range(startRow + 1, endRow) :
                        self._board[flipRow][col] = playerToken
                    return True

        return False
                

    #checks up diagonal row a token was just placed in for flips
    def _checkUpDiagonal(self, row : int, col : int, playerToken : str) -> bool :

        upDiagonalRow = row
        upDiagonalCol = col
        
        if playerToken == gameState.BLACK :
            opponentToken = gameState.WHITE
        else :
            opponentToken = gameState.BLACK

        while upDiagonalCol > 0 and upDiagonalRow < (self._boardRows - 1) :
            upDiagonalRow += 1
            upDiagonalCol -= 1

        #check up diagonal for flips
        countRow = upDiagonalRow
        countCol = upDiagonalCol
        while countRow >= 0 and countCol <=  (self._boardCols - 1) :

            flip = True
            foundTwo = False

            #find first piece
            if self._board[countRow][countCol] == playerToken :
                startRow = countRow
                startCol = countCol
                countRow2 = startRow - 1
                countCol2 = startCol + 1

                #find second piece 
                while countRow2 >= 0 and countCol2 <= (self._boardCols - 1) :
                    if self._board[countRow2][countCol2] == playerToken :
                        foundTwo = True
                        endRow = countRow2
                        endCol = countCol2
                        break
                    
                    countRow2 -= 1
                    countCol2 += 1

                #check values between start and end points for opponents color
                if foundTwo :
                    flipRowCount = startRow - 1
                    flipColCount = startCol + 1

                    while not flipRowCount == endRow :
                        if not self._board[flipRowCount][flipColCount] == opponentToken :
                            flip = False
                            break
                        
                        flipRowCount -= 1
                        flipColCount += 1
                    
            countRow -= 1
            countCol += 1

            #if two pieces are found and opponent pieces are between them
            if foundTwo and flip :
                flipRowCount = startRow
                flipColCount = startCol

                if startCol == col or endCol == col :
                    #check and make sure there is something to flip between
                    if not flipRowCount - 1 == endRow :
                
                        while not flipRowCount == endRow :
                            self._board[flipRowCount][flipColCount] = playerToken
                            flipRowCount -= 1
                            flipColCount += 1
                        return True

                    else :
                        continue

        return False

    #looks for move in the down diagonal that the piece was placed in
    def _checkDownDiagonal(self, row : int, col : int, playerToken : str) -> bool :

        downDiagonalRow = row
        downDiagonalCol = col
        
        if playerToken == gameState.BLACK :
            opponentToken = gameState.WHITE
        else :
            opponentToken = gameState.BLACK

        #find starting coordinates of down diagonal
        while downDiagonalCol > 0 and downDiagonalRow  > 0:
            downDiagonalRow -= 1
            downDiagonalCol -= 1

        #check down diagonal for flips
        countRow = downDiagonalRow
        countCol = downDiagonalCol
        while countRow <= (self._boardRows - 1) and countCol <=  (self._boardCols - 1) :

            flip = True
            foundTwo = False

            #find first piece
            if self._board[countRow][countCol] == playerToken :
                startRow = countRow
                startCol = countCol
                countRow2 = startRow + 1
                countCol2 = startCol + 1

                #find second piece 
                while countRow2 <= (self._boardRows - 1) and countCol2 <= (self._boardCols - 1) :
                    if self._board[countRow2][countCol2] == playerToken :
                        foundTwo = True
                        endRow = countRow2
                        endCol = countCol2
                        break 
                    
                    countRow2 += 1
                    countCol2 += 1

                #check values between start and end points for opponents color
                if foundTwo :
                    flipRowCount = startRow + 1
                    flipColCount = startCol + 1
                    
                    while not flipRowCount == endRow :
                        
                        if not self._board[flipRowCount][flipColCount] == opponentToken :
                            flip = False
                            break
                        
                        flipRowCount += 1
                        flipColCount += 1
                    
            countRow += 1
            countCol += 1

            #if two peices are found and there are opponent pieces between them
            if foundTwo and flip :
                flipRowCount = startRow
                flipColCount = startCol
                
                if startCol == col or endCol == col :
                    #check and make sure there is something to flip between
                    if not flipRowCount + 1 == endRow :
                
                        while not flipRowCount == endRow :
                            self._board[flipRowCount][flipColCount] = playerToken
                            flipRowCount += 1
                            flipColCount += 1
                        return True

                    else :
                        continue

        return False
   
    #detrmine if there are any available moves for the player
    def _checkIfPossibleMove(self, playerToken : str) -> bool :

        foundFlip = False
        originalBoard = copy.deepcopy(self._board)
        
        for row in range(1,self._boardRows + 1) :

            for col in range(1,self._boardCols + 1) :

                if self._isEmpty(row - 1, col - 1) :
                    foundFlip = self._makeMove(playerToken, row, col)
                    self._board[row - 1][col - 1] = ' '

                if foundFlip :
                    self._board = originalBoard
                    return True

        return False
            

    def _isEmpty(self, row : int, col : int) -> bool :

        if self._board[row][col] == ' ' :
            return True
        else :
            return False

    def _isBoardFull(self, gameType : 'gameTypeTuple') -> bool :

        numBlack, numWhite = self._countPieces()
        boardFull = numBlack + numWhite == self._boardRows * self._boardCols

        if boardFull :
            return True

        return False
        

    def _countPieces(self) -> int:

        numBlack = 0
        numWhite = 0

        for row in range(self._boardRows) :

            for col in range(self._boardCols) :

                if self._board[row][col] is gameState.BLACK :
                    numBlack += 1
                elif self._board[row][col] is gameState.WHITE :
                    numWhite += 1

        return numBlack, numWhite
