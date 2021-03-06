class ChessManagement(object):
    def __init__(self):
        super().__init__()
        self.board = {}
        self.listpiece = {}
        self.board_black = {
            'BR1':{'curpos':(0,0), 'posspos':{}, 'moved':False, 'killable':False, 'score':6.0, 'range':{(1,0),(0,1)}},
            'BK1':{'curpos':(0,1), 'posspos':{(2,0),(2,2)}, 'killable':False, 'moved':False, 'score':4.5, 'range':{(1,3)}},
            'BB1':{'curpos':(0,2), 'posspos':{}, 'moved':False, 'killable':False, 'score':4.5, 'range':{(1,1),(1,3)}},
            'BQ':{'curpos':(0,3), 'posspos':{}, 'moved':False, 'killable':False, 'score':11.0, 'range':{(0,2),(1,2),(1,3),(1,4),(0,4)}},
            'BX':{'curpos':(0,4), 'posspos':{}, 'moved':False, 'killable':False, 'score':10000.0, 'range':{(0,3),(1,3),(1,4),(1,5),(0,5)}},
            'BB2':{'curpos':(0,5), 'posspos':{}, 'moved':False, 'killable':False, 'score':5.0, 'range':{(1,4),(1,6)}},
            'BK2':{'curpos':(0,6), 'posspos':{(2,5),(2,7)}, 'moved':False, 'killable':False, 'score':4.5, 'range':{(1,4)}},
            'BR2':{'curpos':(0,7), 'posspos':{}, 'moved':False, 'killable':False, 'score':7.0, 'range':{(1,7), (0,6)}},
            'BP1':{'curpos':(1,0), 'posspos':{(2,0),(3,0)}, 'moved':False, 'killable':False, 'score':0.5, 'range':{(2,1),(3,1)}},
            'BP2':{'curpos':(1,1), 'posspos':{(2,1),(3,1)}, 'moved':False, 'killable':False, 'score':0.5, 'range':{(2,0),(3,0),(2,2),(3,2)}},
            'BP3':{'curpos':(1,2), 'posspos':{(2,2),(3,2)}, 'moved':False, 'killable':False, 'score':0.5, 'range':{(2,1),(3,1),(2,3),(3,3)}},
            'BP4':{'curpos':(1,3), 'posspos':{(2,3),(3,3)}, 'moved':False, 'killable':False, 'score':0.5, 'range':{(2,2),(3,2),(2,4),(3,4)}},
            'BP5':{'curpos':(1,4), 'posspos':{(2,4),(3,4)}, 'moved':False, 'killable':False, 'score':0.5, 'range':{(2,3),(3,3),(2,5),(3,5)}},
            'BP6':{'curpos':(1,5), 'posspos':{(2,5),(3,5)}, 'moved':False, 'killable':False, 'score':0.5, 'range':{(2,4),(3,4),(2,6),(3,6)}},
            'BP7':{'curpos':(1,6), 'posspos':{(2,6),(3,6)}, 'moved':False, 'killable':False, 'score':0.5, 'range':{(2,5),(3,5),(2,7),(3,7)}},
            'BP8':{'curpos':(1,7), 'posspos':{(2,7),(3,7)}, 'moved':False, 'killable':False, 'score':0.5, 'range':{(2,6),(3,6)}}
        }
        self.board_white = {
            'WP1':{'curpos':(6,0), 'posspos':{(5,0),(4,0)}, 'moved':False, 'killable':False, 'score':0.5, 'range':{(5,1),(4,1)}},
            'WP2':{'curpos':(6,1), 'posspos':{(5,1),(4,1)}, 'moved':False, 'killable':False, 'score':0.5, 'range':{(5,0),(4,0),(5,2),(4,2)}},
            'WP3':{'curpos':(6,2), 'posspos':{(5,2),(4,2)}, 'moved':False, 'killable':False, 'score':0.5, 'range':{(5,1),(4,1),(5,3),(4,3)}},
            'WP4':{'curpos':(6,3), 'posspos':{(5,3),(4,3)}, 'moved':False, 'killable':False, 'score':0.5, 'range':{(5,2),(4,2),(5,4),(4,4)}},
            'WP5':{'curpos':(6,4), 'posspos':{(5,4),(4,4)}, 'moved':False, 'killable':False, 'score':0.5, 'range':{(5,3),(4,3),(5,5),(4,5)}},
            'WP6':{'curpos':(6,5), 'posspos':{(5,5),(4,5)}, 'moved':False, 'killable':False, 'score':0.5, 'range':{(5,4),(4,4),(5,6),(4,6)}},
            'WP7':{'curpos':(6,6), 'posspos':{(5,6),(4,6)}, 'moved':False, 'killable':False, 'score':0.5, 'range':{(5,5),(4,5),(5,7),(4,7)}},
            'WP8':{'curpos':(6,7), 'posspos':{(5,7),(4,7)}, 'moved':False, 'killable':False, 'score':0.5, 'range':{(5,6),(4,6)}},
            'WR1':{'curpos':(7,0), 'posspos':{}, 'moved':False, 'killable':False, 'score':6.0, 'range':{(6,0),(7,1)}},
            'WK1':{'curpos':(7,1), 'posspos':{(5,0),(5,2)}, 'moved':False, 'killable':False, 'score':4.5, 'range':{(6,3)}},
            'WB1':{'curpos':(7,2), 'posspos':{}, 'moved':False, 'killable':False, 'score':4.5, 'range':{(6,1),(6,3)}},
            'WQ':{'curpos':(7,3), 'posspos':{}, 'moved':False, 'killable':False, 'score':11.0, 'range':{(7,2),(6,2),(6,3),(6,4),(7,4)}},
            'WX':{'curpos':(7,4), 'posspos':{}, 'moved':False, 'killable':False, 'score':10000.0, 'range':{(7,3),(6,3),(6,4),(6,5),(7,5)}},
            'WB2':{'curpos':(7,5), 'posspos':{}, 'moved':False, 'killable':False, 'score':5.0, 'range':{(6,4),(6,6)}},
            'WK2':{'curpos':(7,6), 'posspos':{(5,5),(5,7)}, 'moved':False, 'killable':False, 'score':4.5, 'range':{(6,4)}},
            'WR2':{'curpos':(7,7), 'posspos':{}, 'moved':False, 'killable':False, 'score':7.0, 'range':{(6,7), (7,6)}}
        }
        self.regeneration_score = {
            'R': 7.0,
            'K': 4.5,
            'B': 6.5,
            'Q': 11.0
        }

    def getBoard(self):
        return self.board

    def createBoardState(self, savedBoardState = None):
        boardState = []
        if savedBoardState is not None:
            self.board_black = {}
            self.board_white = {}

            for key, value in savedBoardState.boardstate.items():
                boardToProcess = self.board_white if key.startswith('W') else self.board_black
                boardToProcess[key] = {
                    'curpos': value.curpos,
                    'posspos': value.posspos,
                    'moved': value.moved,
                    'score': value.score,
                    'range': value.range,
                    'killable': value.killable
                }

        self.board = {**self.board_black, **self.board_white}

        for key, value in self.board.items():
            s=list(value["curpos"])
            s.append(key)
            boardState.append(s)
        return boardState

    def showMoves(self, request):
        listpiece = {}
        piece = request.form['piece']
        listpiece["posspos"]=list(self.board[piece]["posspos"])
        listpiece["range"]=list(self.board[piece]["range"])
        listpiece["killable"] = [self.board[x]['curpos'] for x in self.board.keys() if self.board[x]['killable'] is True]
        return listpiece

    def movePiece(self, request, counter=None):
        listpiece = {}
        move = request.form['move']
        cut = request.form['cut']
        replaced = request.form['replaced']
        if counter is not None:
            replaced = replaced + str(counter)
        i = int(request.form['i'])
        j = int(request.form['j'])

        # Temporary object - Purpose: to store previous location in database
        listpiece['prevloc'] = self.board[move]["curpos"]
        listpiece['status'] = ''

        if move[0] == "W":
            if cut != "":
                self.board_black[cut] = {
                    'curpos':(-1,-1), 'posspos':{}, 
                    'moved':self.board_black[cut]['moved'], 
                    'score':self.board_black[cut]['score'], 
                    'killable':False,
                    'range':{}
                }
            # Special Case: Pawn moves 2 steps (En-passant move)
            if move[1] == "P" and not self.board_white[move]["moved"] \
                and (self.board_white[move]["curpos"][0] - i) > 1:
                curpos = [value['curpos'] for key, value in self.board_black.items() if key[1] == 'P']
                if (i, j+1) in curpos or (i, j-1) in curpos:
                    self.board_white[move]["killable"] = True
                    self.board_white[move]["curpos"] = (i, j)
                else:
                    self.board_white[move]["curpos"] = (i, j)
            # Special Case: Pawn reached last row
            elif replaced != "":
                self.board_white[move] = {
                    'curpos':(-1,-1), 'posspos':{}, 
                    'moved':self.board_white[move]['moved'], 
                    'score':self.board_white[move]['score'], 'range':{}
                }
                self.board_white[replaced] = {}
                self.board_white[replaced]["curpos"] = (i, j)
                self.board_white[replaced]["moved"] = True
                self.board_white[replaced]['score'] = self.regeneration_score[replaced[1]]
                self.board_white[replaced]['range'] = {}
                listpiece["replaced"] = replaced
            # Special Case: Castling to the right
            elif move[1] == "X" and (j - self.board_white[move]["curpos"][1]) > 1:
                self.board_white[move]["curpos"] = (i, j)
                self.board_white['WR2']['curpos'] = (i, 5)
                self.board_white['WR2']['moved'] = True
            # Special Case: Castling to the left
            elif move[1] == "X" and (self.board_white[move]["curpos"][1] - j) > 1:
                self.board_white[move]["curpos"] = (i, j)
                self.board_white['WR1']['curpos'] = (i, 3)
                self.board_white['WR1']['moved'] = True
            else:
                self.board_white[move]["curpos"] = (i, j)

            self.board_white[move]["moved"] = True

            for _ in self.board_black.keys():
                self.board_black[_]['killable'] = False
        else:
            if cut != "":
                self.board_white[cut] = {
                    'curpos':(-1,-1), 'posspos':{}, 
                    'moved':self.board_white[cut]['moved'], 
                    'score':self.board_white[cut]['score'],
                    'killable':False,
                    'range':{}
                }
            # Special Case: Pawn moves 2 steps (En-passant move)
            if move[1] == "P" and not self.board_black[move]["moved"] \
                and (i - self.board_black[move]["curpos"][0]) > 1:
                curpos = [value['curpos'] for key, value in self.board_white.items() if key[1] == 'P']
                if (i, j+1) in curpos or (i, j-1) in curpos:
                    self.board_black[move]["killable"] = True
                    self.board_black[move]["curpos"] = (i, j)
                else:
                    self.board_black[move]["curpos"] = (i, j)
            # Special Case: Pawn reached last row
            elif replaced != "":
                self.board_black[move] = {
                    'curpos':(-1,-1), 'posspos':{}, 
                    'moved':self.board_black[move]['moved'], 
                    'score':self.board_black[move]['score'], 
                    'range':{}
                }
                self.board_black[replaced] = {}
                self.board_black[replaced]["curpos"] = (i, j)
                self.board_black[replaced]["moved"] = True
                self.board_black[replaced]['score'] = self.regeneration_score[replaced[1]]
                self.board_black[replaced]['range'] = {}
                listpiece["replaced"] = replaced
            # Special Case: Castling to the right
            elif move[1] == "X" and (self.board_black[move]["curpos"][1] - j) > 1:
                self.board_black[move]["curpos"] = (i, j)
                self.board_black['BR1']['curpos'] = (i, 3)
                self.board_black['BR1']['moved'] = True
            # Special Case: Castling to the left
            elif move[1] == "X" and (j - self.board_black[move]["curpos"][1]) > 1:
                self.board_black[move]["curpos"] = (i, j)
                self.board_black['BR2']['curpos'] = (i, 5)
                self.board_black['BR2']['moved'] = True
            else:
                self.board_black[move]["curpos"] = (i, j)

            self.board_black[move]["moved"] = True

            for _ in self.board_white.keys():
                self.board_white[_]['killable'] = False

        listpiece["boardState"] = self.createBoardState()
        listpiece["whoToMove"] = "W" if move[0] == "B" else "B"
        self.generatePossibleMoves()

        # Check if king is still under check after move?
        # If yes, mark game as lost
        boardToProcess  = self.board_black if move[0] == "B" else self.board_white
        boardToKill     = self.board_black if move[0] == "W" else self.board_white
        whichKing       = "BX" if move[0] == "B" else "WX"
        kingPos         = boardToProcess[whichKing]['curpos']
        killPos         = [set(x['posspos']) for x in boardToKill.values()]
        killPos         = list(set.union(*killPos)) # All possible positions of attackers allies
        if kingPos in killPos:
            listpiece['status'] = 'Mate'

        # Check for checkmate iff game is not already lost
        if listpiece['status'] == '':
            pieceCausingCheckMate = replaced if replaced != "" else move 
            boardToKill = self.board_white if listpiece["whoToMove"] == 'B' else self.board_black
            kingPos = self.board[listpiece["whoToMove"]+'X']['curpos']
            killPos = [x['posspos'] for x in boardToKill.values()]
            killPos = list(set.union(*killPos)) # All possible positions of attackers allies
            if kingPos in killPos and self.isCheckMated(listpiece["whoToMove"], pieceCausingCheckMate):
                    listpiece['status'] = 'Checkmate'
        
        return listpiece

    def generatePossibleMoves(self):
        for _ in self.board.keys():
            if self.board[_]['curpos'] not in ((-1,-1),):
                if _[1] == 'K':
                    self.generateKnightMoves(_)
                elif _[1] == 'P':
                    self.generatePawnMoves(_)
                elif _[1] == 'R':
                    self.generateRookMoves(_)
                elif _[1] == 'B':
                    self.generateBishopMoves(_)
                elif _[1] == 'Q':
                    self.generateBishopMoves(_)
                    self.generateRookMoves(_, extend=True)
                elif _[1] == 'X':
                    self.generateKingMoves(_)

    def generatePawnMoves(self, piece):
        """Parameters:
        -----------
        piece: piece name in string format.

        Usage:
        -----------
        Used to generate possible moves for a pawn. 
        Updates curpos key with all possible locations where selected pawn (piece) can move on board.
        """
        posspos = set()
        prange = set()
        whoToMove = piece[0]
        i, j = self.board[piece]['curpos']
        boardToProcess = self.board_black if whoToMove == "B" else self.board_white
        boardToKill = self.board_black if whoToMove == "W" else self.board_white
        curposList = [x['curpos'] for x in self.board.values()]
        curposProcessList = [x['curpos'] for x in boardToProcess.values()]
        curposKillList = [x['curpos'] for x in boardToKill.values()]
        movable = True
        if whoToMove == "B":
            #If en-passant position is available for kill, add it to possible moves
            if j+1 < 8:
                pieces = [key for key, value in boardToKill.items() if key[1] == 'P' and (i, j+1) == value['curpos'] and value['killable'] is True]
                if len(pieces) > 0:
                    posspos.add((i+1, j+1))
            #If en-passant position is available for kill, add it to possible moves
            if j-1 >= 0:
                pieces = [key for key, value in boardToKill.items() if key[1] == 'P' and (i, j-1) == value['curpos'] and value['killable'] is True]
                if len(pieces) > 0:
                    posspos.add((i+1, j-1))
            # If the next position is blank, add it in possible moves
            if i+1 < 8 and (i+1, j) not in curposList:
                posspos.add((i+1, j))
            # else:
            #     # Mark movable to False so that special kill position is marked invalid
            #     # when pawn can move 2 places
            #     movable = False
            if i+1 < 8:
                # if next bottom right cell contains white piece, add that location to possible moves
                if j+1 < 8 and (i+1, j+1) in curposKillList:
                    posspos.add((i+1, j+1))
                # if next bottom right cell contains black piece, add that location to possible range
                if j+1 < 8 and (i+1, j+1) in curposProcessList:
                    prange.add((i+1, j+1))
                # if next bottom left cell contains white piece, add that location to possible moves
                if j-1 >= 0 and (i+1, j-1) in curposKillList:
                    posspos.add((i+1, j-1))
                # if next bottom left cell contains white piece, add that location to possible range
                if j-1 >= 0 and (i+1, j-1) in curposProcessList:
                    prange.add((i+1, j-1))
            # if this pawn is never moved before
            if not boardToProcess[piece]['moved']:
                # if next to next row (same column) is blank, add it to possible moves
                if i+2 < 8 and (i+1, j) not in curposList and (i+2, j) not in curposList:
                    posspos.add((i+2, j))
                # else:
                #     # Mark movable to False so that special kill position is marked invalid
                #     # when pawn can move 2 places and kill piece in adjacent column
                #     movable = False
                # if i+2 < 8 and movable:
                #     # if next to next bottom right cell contains white piece, add that location to possible moves
                #     if j+1 < 8 and (i+2, j+1) in curposKillList:
                #         posspos.add((i+2, j+1))
                #     # if next to next bottom right cell contains black piece, add that location to possible range
                #     if j+1 < 8 and (i+2, j+1) in curposProcessList:
                #         prange.add((i+2, j+1))
                #     # if next to next bottom left cell contains white piece, add that location to possible moves
                #     if j-1 >= 0 and (i+2, j-1) in curposKillList:
                #         posspos.add((i+2, j-1))
                #     # if next to next bottom left cell contains white piece, add that location to possible range
                #     if j-1 >= 0 and (i+2, j-1) in curposProcessList:
                #         prange.add((i+2, j-1))
        else:
            #If en-passant position is available for kill, add it to possible moves
            if j+1 < 8:
                pieces = [key for key, value in boardToKill.items() if key[1] == 'P' and (i, j+1) == value['curpos'] and value['killable'] is True]
                if len(pieces) > 0:
                    posspos.add((i-1, j+1))
            #If en-passant position is available for kill, add it to possible moves
            if j-1 >= 0:
                pieces = [key for key, value in boardToKill.items() if key[1] == 'P' and (i, j-1) == value['curpos'] and value['killable'] is True]
                if len(pieces) > 0:
                    posspos.add((i-1, j-1))
            # If the next position is blank, add it in possible moves
            if i-1 >= 0 and (i-1, j) not in curposList:
                posspos.add((i-1, j))
            # else:
            #     # Mark movable to False so that special kill position is marked invalid
            #     # when pawn can move 2 places and kill piece in adjacent column
            #     movable = False
            if i-1 >= 0:
                # if next top right cell contains black piece, add that location to possible moves
                if j+1 < 8 and (i-1, j+1) in curposKillList:
                    posspos.add((i-1, j+1))
                # if next top right cell contains white piece, add that location to possible range
                if j+1 < 8 and (i-1, j+1) in curposProcessList:
                    prange.add((i-1, j+1))
                # if next top left cell contains black piece, add that location to possible moves
                if j-1 >= 0 and (i-1, j-1) in curposKillList:
                    posspos.add((i-1, j-1))
                # if next top left cell contains white piece, add that location to possible range
                if j-1 >= 0 and (i-1, j-1) in curposProcessList:
                    prange.add((i-1, j-1))
            # if this pawn is never moved before
            if not boardToProcess[piece]['moved']:
                # if next to next row (same column) is blank, add it to possible moves
                if i-2 >= 0 and (i-1, j) not in curposList and (i-2, j) not in curposList:
                    posspos.add((i-2, j))
        boardToProcess[piece]['posspos'] = posspos
        boardToProcess[piece]['range'] = prange

    def generateBishopMoves(self, piece):
        """Parameters:
        -----------
        piece: piece name in string format.

        Usage:
        -----------
        Used to generate possible moves for a bishop. 
        Updates curpos key with all possible locations where selected bishop (piece) can move on board.
        """
        posspos = set()
        prange = set()
        whoToMove = piece[0]
        i, j = self.board[piece]['curpos']
        boardToProcess = self.board_black if whoToMove == "B" else self.board_white
        boardToKill = self.board_black if whoToMove == "W" else self.board_white
        curposList = [x['curpos'] for x in self.board.values()]
        curposProcessList = [x['curpos'] for x in boardToProcess.values()]
        curposKillList = [x['curpos'] for x in boardToKill.values()]
        # Diagonal bottom right - Possible Moves and Ranges
        for x in range(1, 8):
            if i+x < 8 and j+x < 8 and (i+x, j+x) not in curposList:
                posspos.add((i+x, j+x))
            elif (i+x, j+x) in curposKillList:
                posspos.add((i+x, j+x))
                break
            elif (i+x, j+x) in curposProcessList:
                prange.add((i+x, j+x))
                break
            else:
                break
        # Diagonal top left - Possible Moves and Ranges
        for x in range(1, 8):
            if i-x >= 0 and j-x >= 0 and (i-x, j-x) not in curposList:
                posspos.add((i-x, j-x))
            elif (i-x, j-x) in curposKillList:
                posspos.add((i-x, j-x))
                break
            elif (i-x, j-x) in curposProcessList:
                prange.add((i-x, j-x))
                break
            else:
                break
        # Diagonal bottom left - Possible Moves and Ranges
        for x in range(1, 8):
            if i+x < 8 and j-x >= 0 and (i+x, j-x) not in curposList:
                posspos.add((i+x, j-x))
            elif (i+x, j-x) in curposKillList:
                posspos.add((i+x, j-x))
                break
            elif (i+x, j-x) in curposProcessList:
                prange.add((i+x, j-x))
                break
            else:
                break
        # Diagonal top right - Possible Moves and Ranges
        for x in range(1, 8):
            if i-x >= 0 and j+x < 8 and (i-x, j+x) not in curposList:
                posspos.add((i-x, j+x))
            elif (i-x, j+x) in curposKillList:
                posspos.add((i-x, j+x))
                break
            elif (i-x, j+x) in curposProcessList:
                prange.add((i-x, j+x))
                break
            else:
                break
        boardToProcess[piece]['posspos'] = posspos
        boardToProcess[piece]['range'] = prange

    def generateRookMoves(self, piece, extend=False):
        """Parameters:
        -----------
        piece: piece name in string format.

        Usage:
        -----------
        Used to generate possible moves for a rook. 
        Updates curpos key with all possible locations where selected rook (piece) can move on board.
        """
        posspos = set()
        prange = set()
        whoToMove = piece[0]
        i, j = self.board[piece]['curpos']
        boardToProcess = self.board_black if whoToMove == "B" else self.board_white
        boardToKill = self.board_black if whoToMove == "W" else self.board_white
        curposList = [x['curpos'] for x in self.board.values()]
        curposProcessList = [x['curpos'] for x in boardToProcess.values()]
        curposKillList = [x['curpos'] for x in boardToKill.values()]
        # Down Rows
        for x in range(i+1, 8):
            if (x, j) not in curposList:
                posspos.add((x, j))
            elif (x, j) in curposKillList:
                posspos.add((x, j))
                break
            elif (x, j) in curposProcessList:
                prange.add((x, j))
                break
            else:
                break
        # Up Rows
        for x in range(i-1, -1, -1):
            if (x, j) not in curposList:
                posspos.add((x, j))
            elif (x, j) in curposKillList:
                posspos.add((x, j))
                break
            elif (x, j) in curposProcessList:
                prange.add((x, j))
                break
            else:
                break
        # Right Columns
        for x in range(j+1, 8):
            if (i, x) not in curposList:
                posspos.add((i, x))
            elif (i, x) in curposKillList:
                posspos.add((i, x))
                break
            elif (i, x) in curposProcessList:
                prange.add((i, x))
                break
            else:
                break
        # Left Columns
        for x in range(j-1, -1, -1):
            if (i, x) not in curposList:
                posspos.add((i, x))
            elif (i, x) in curposKillList:
                posspos.add((i, x))
                break
            elif (i, x) in curposProcessList:
                prange.add((i, x))
                break
            else:
                break
        if extend:
            boardToProcess[piece]['posspos'] = boardToProcess[piece]['posspos'].union(posspos)
            boardToProcess[piece]['range'] = boardToProcess[piece]['range'].union(prange)
        else:
            boardToProcess[piece]['posspos'] = posspos
            boardToProcess[piece]['range'] = prange

    def generateKnightMoves(self, piece):
        """Parameters:
        -----------
        piece: piece name in string format.

        Usage:
        -----------
        Used to generate possible moves for a knight. 
        Updates curpos key with all possible locations where selected knight (piece) can move on board.
        """
        posspos = set()
        prange = set()
        whoToMove = piece[0]
        i, j = self.board[piece]['curpos']
        boardToProcess = self.board_black if whoToMove == "B" else self.board_white
        curposList = [x['curpos'] for x in boardToProcess.values()]
        if i+2 < 8:
            if j+1 < 8:
                if (i+2, j+1) not in curposList:
                    posspos.add((i+2, j+1))
                elif (i+2, j+1) in curposList:
                    prange.add((i+2, j+1))
            if j-1 >= 0:
                if (i+2, j-1) not in curposList:
                    posspos.add((i+2, j-1))
                elif (i+2, j-1) in curposList:
                    prange.add((i+2, j-1))
        if i-2 >= 0:
            if j+1 < 8:
                if (i-2, j+1) not in curposList:
                    posspos.add((i-2, j+1))
                elif (i-2, j+1) in curposList:
                    prange.add((i-2, j+1))
            if j-1 >= 0:
                if (i-2, j-1) not in curposList:
                    posspos.add((i-2, j-1))
                elif (i-2, j-1) in curposList:
                    prange.add((i-2, j-1))
        if i+1 < 8:
            if j+2 < 8:
                if (i+1, j+2) not in curposList:
                    posspos.add((i+1, j+2))
                elif (i+1, j+2) in curposList:
                    prange.add((i+1, j+2))
            if j-2 >= 0:
                if (i+1, j-2) not in curposList:
                    posspos.add((i+1, j-2))
                elif (i+1, j-2) in curposList:
                    prange.add((i+1, j-2))
        if i-1 >= 0:
            if j+2 < 8:
                if (i-1, j+2) not in curposList:
                    posspos.add((i-1, j+2))
                elif (i-1, j+2) in curposList:
                    prange.add((i-1, j+2))
            if j-2 >= 0:
                if (i-1, j-2) not in curposList:
                    posspos.add((i-1, j-2))
                elif (i-1, j-2) in curposList:
                    prange.add((i-1, j-2))
        boardToProcess[piece]['posspos'] = posspos
        boardToProcess[piece]['range'] = prange

    def generateKingMoves(self, piece):
        """Parameters:
        -----------
        piece: piece name in string format.

        Usage:
        -----------
        Used to generate possible moves for a king. 
        Updates curpos key with all possible locations where selected king (piece) can move on board.
        """
        posspos = set()
        prange = set()
        whoToMove = piece[0]
        i, j = self.board[piece]['curpos']
        boardToProcess = self.board_black if whoToMove == "B" else self.board_white
        boardToKill = self.board_black if whoToMove == "W" else self.board_white
        curposList = [x['curpos'] for x in boardToProcess.values()]
        killposList = [set(x['posspos']) for x in boardToKill.values()]
        killposList = list(set.union(*killposList))
        allposList = [x['curpos'] for x in self.board.values()]
        isKingAndRook1Moved = self.board[piece]['moved'] or self.board[whoToMove+'R1']['moved']
        isKingAndRook2Moved = self.board[piece]['moved'] or self.board[whoToMove+'R2']['moved']

        if not isKingAndRook1Moved:
            if (i, j+1) not in allposList and (i, j+2) not in allposList \
                and (i, j+1) not in killposList and (i, j+2) not in killposList:
                posspos.add((i, j+2))

        if not isKingAndRook2Moved:
            if (i, j-1) not in allposList and (i, j-2) not in allposList and (i, j-3) not in allposList \
                (i, j-1) not in killposList and (i, j-2) not in killposList and (i, j-3) not in killposList:
                posspos.add((i, j-2))

        for x in range(i-1, i+2):
            for y in range(j-1, j+2):
                if x >= 0 and x < 8 and y >= 0 and y < 8 and (x, y) not in curposList:
                        posspos.add((x, y))
                elif x >= 0 and x < 8 and y >= 0 and y < 8 and (x, y) in curposList:
                        prange.add((x, y))
        boardToProcess[piece]['posspos'] = posspos
        boardToProcess[piece]['range'] = prange

    def isCheckMated(self, whoToMove, piece):
        boardToProcess = self.board_black if whoToMove == "B" else self.board_white
        boardToKill = self.board_black if whoToMove == "W" else self.board_white
        kingPiece = boardToProcess[whoToMove+"X"]       # Object of King under attack
        kingPos = kingPiece['curpos']                   # position of King under attack
        piecePos = self.board[piece]['curpos']          # position of piece attacking King

        # 1.a. Can the piece causing CheckMate be killed by any other piece except King itself?
        possposList = [boardToProcess[x]['posspos'] for x in boardToProcess.keys() if x[1] != "X"]
        possposList = list(set.union(*possposList)) # All possible positions of attackers allies
        canPieceBeKilled = piecePos in possposList  # if attacking piece is in line of fire of allies
        # If piece can be killed, it is not a checkmate yet
        if canPieceBeKilled:
            return False

        # 1.b. Can the piece causing CheckMate be killed by King itself?
        kingPossPos = kingPiece['posspos']
        if piecePos in kingPossPos:
            possRangeList = [x['range'] for x in boardToKill.values()]
            possRangeList = list(set.union(*possRangeList)) # All possible positions of attackers allies
            isPieceBacked = piecePos in possRangeList  # if attacking piece is backed by it's allies
            # If piece is not backed by allies and can be killed, it is not a checkmate yet
            if isPieceBacked:
                return False

        # 2. Can any other piece block the path?
        # If attacker is a Knight, well, the king is screwed. Nobody can block it
        # If attacker is a Rook
        if piece[1] == "R":
            attackByRook = self.attackByRook(whoToMove, piece)
            if attackByRook is False:
                return False
        # If attacker is a Bishop
        elif piece[1] == "B":
            attackByBishop = self.attackByBishop(whoToMove, piece)
            if attackByBishop is False:
                return False
        # If attacker is a Queen
        elif piece[1] == "Q":
            print("Attacked by Queen")
            attackByRook = self.attackByRook(whoToMove, piece)
            attackByBishop = self.attackByBishop(whoToMove, piece)
            if attackByRook is False or attackByBishop is False:
                return False

        # 3. Can King Move?
        possposList = [x['posspos'] for x in boardToKill.values()]
        possposList = list(set.union(*possposList))
        if kingPiece['curpos'] in possposList:
            allList = [pos in possposList for pos in kingPiece['posspos']]
            isKingSurrounded = all(allList)
            return isKingSurrounded

        return False

    def attackByRook(self, whoToMove, piece):
        print(f'whoToMove: {whoToMove}, piece: {piece}')
        boardToProcess = self.board_black if whoToMove == "B" else self.board_white
        curposList = self.board[piece]['posspos']
        possposList = [boardToProcess[x]['posspos'] for x in boardToProcess.keys() if x[1] != "X"]
        possposList = list(set.union(*possposList))     # All possible positions of attackers allies
        kingPiece = boardToProcess[whoToMove+"X"]       # Object of King under attack
        kingPos = kingPiece['curpos']                   # position of King under attack
        piecePos = self.board[piece]['curpos']          # position of piece attacking King
        print(f'kingPiece: {kingPiece}')
        print(f'kingPos: {kingPos}')
        print(f'piecePos: {piecePos}')
        print(f'curposList: {curposList}')
        print(f'possposList: {possposList}')

        # If they both are in same row
        if kingPos[0] == piecePos[0]:
            # if king is after attacker
            if kingPos[1] > piecePos[1]:
                for i in range(piecePos[1]+1, kingPos[1]):
                    print(kingPos[0], i)
                    if (kingPos[0], i) in possposList:
                        return False
            # if king is before attacker
            elif kingPos[1] < piecePos[1]:
                for i in range(kingPos[1]+1, piecePos[1]):
                    if (kingPos[0], i) in possposList:
                        return False
        # If they both are in same column
        elif kingPos[1] == piecePos[1]:
            # if king is after attacker
            if kingPos[0] > piecePos[0]:
                for i in range(piecePos[0]+1, kingPos[0]):
                    if (i, kingPos[1]) in possposList:
                        return False
            # if king is before attacker
            elif kingPos[0] < piecePos[0]:
                for i in range(kingPos[0]+1, piecePos[0]):
                    if (kingPos[1], i) in possposList:
                        return False
        return True

    def attackByBishop(self, whoToMove, piece):
        boardToProcess = self.board_black if whoToMove == "B" else self.board_white
        curposList = self.board[piece]['posspos']
        possposList = [boardToProcess[x]['posspos'] for x in boardToProcess.keys() if x[1] != "X"]
        kingPiece = boardToProcess[whoToMove+"X"]       # Object of King under attack
        kingPos = kingPiece['curpos']                   # position of King under attack
        piecePos = self.board[piece]['curpos']          # position of piece attacking King
        # If King position is top left of attacker
        if kingPos[0] < piecePos[0] and kingPos[1] < piecePos[1]:
            for i in range(kingPos[0]+1, piecePos[0]):
                for j in range(kingPos[1]+1, piecePos[1]):
                    if (i, j) in possposList:
                        return False
        # If King position is top right of attacker
        elif kingPos[0] < piecePos[0] and kingPos[1] > piecePos[1]:
            for i in range(kingPos[0]+1, piecePos[0]):
                for j in range(piecePos[1]+1, kingPos[1]):
                    if (i, j) in possposList:
                        return False
        # If King position is bottom left of attacker
        if kingPos[0] > piecePos[0] and kingPos[1] < piecePos[1]:
            for i in range(piecePos[0]+1, kingPos[0]):
                for j in range(kingPos[1]+1, piecePos[1]):
                    if (i, j) in possposList:
                        return False
        # If King position is bottom right of attacker
        elif kingPos[0] > piecePos[0] and kingPos[1] > piecePos[1]:
            for i in range(piecePos[0]+1, kingPos[0]):
                for j in range(piecePos[1]+1, kingPos[1]):
                    if (i, j) in possposList:
                        return False
        return True
