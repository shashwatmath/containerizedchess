from cassandra.cluster import Cluster, BatchStatement
from cassandra import ConsistencyLevel
from cassandra.query import SimpleStatement
from uuid import uuid1, UUID
from random import choice
from string import ascii_letters
from datetime import datetime
from copy import deepcopy
from json import loads

class DatabaseManagement(object):
    def __init__(self):
        super().__init__()
        self.session = None
        self.KEYSPACENAME = 'docker'
        self.connectionList = ['172.18.0.2', '172.18.0.3']
        self.cluster = None
        self.PAGE_LIMIT = 10

    def loadDatabase(self):
        self.cluster = Cluster(self.connectionList)
        # self.cluster = Cluster()
        self.session = self.cluster.connect()
        keyspace = "CREATE KEYSPACE IF NOT EXISTS %s WITH replication = \
                    {'class': 'NetworkTopologyStrategy', 'dc1': '1', 'dc2': '1'} \
                        AND durable_writes = true;"%(self.KEYSPACENAME, )
        self.session.execute(keyspace)

        self.session.execute(f"USE {self.KEYSPACENAME};")

        pieceState = "CREATE TYPE IF NOT EXISTS pieceState ( \
                    curpos tuple<int, int>, \
                    posspos set<frozen<tuple<int, int>>>, \
                    moved boolean, \
                    killable boolean, \
                    score double, \
                    range set<frozen<tuple<int, int>>> \
                    )"

        self.session.execute(pieceState)

        user = "CREATE TABLE IF NOT EXISTS users ( \
                userid text PRIMARY KEY, \
                password text, \
                email text, \
                friends set<text> \
                )"

        self.session.execute(user)

        mvemailusers = "CREATE MATERIALIZED VIEW IF NOT EXISTS mvemailusers as \
                SELECT * FROM users \
                where email is not null \
                PRIMARY KEY (email, userid);"

        print(f'mvemailusers: {mvemailusers}')
        self.session.execute(mvemailusers)

        chessgame = "CREATE TABLE IF NOT EXISTS chessgame ( \
                gamecode uuid PRIMARY KEY, \
                gamedate timeuuid, \
                previousblackmove tuple<int, int>, \
                previouswhitemove tuple<int, int>, \
                gameturn text, \
                userid text, \
                opponentid text, \
                isactive boolean, \
                ispublic boolean, \
                starttime timestamp, \
                endtime timestamp, \
                status text, \
                wonby text \
                )"

        self.session.execute(chessgame)

        indexispublicchessgame = "CREATE INDEX IF NOT EXISTS indexispublicchessgame \
                ON chessgame(ispublic)"

        self.session.execute(indexispublicchessgame)

        boardstate = "CREATE TABLE IF NOT EXISTS boardstate ( \
                gamecode uuid, \
                movetime timeuuid, \
                piece text, \
                prevloc tuple<int, int>, \
                newloc tuple<int, int>, \
                piececut text, \
                replaced text, \
                boardstate map<text, frozen<pieceState>>, \
                PRIMARY KEY (gamecode, movetime) \
                ) WITH CLUSTERING ORDER BY (movetime DESC)"

        self.session.execute(boardstate)

        userstats = "CREATE TABLE IF NOT EXISTS userstats ( \
                userid text PRIMARY KEY, \
                wins counter, \
                losses counter, \
                draws counter, \
                surrenders counter \
                )"

        self.session.execute(userstats)

        gamestats = "CREATE TABLE IF NOT EXISTS gamestats ( \
                gamecode uuid PRIMARY KEY, \
                totalblackmoves counter, \
                totalwhitemoves counter, \
                regeneratedblackrooks counter, \
                regeneratedblackkinghts counter, \
                regeneratedblackbishops counter, \
                regeneratedblackqueens counter, \
                regeneratedwhiterooks counter, \
                regeneratedwhitekinghts counter, \
                regeneratedwhitebishops counter, \
                regeneratedwhitequeens counter \
                )"

        self.session.execute(gamestats)

        userheadonstats = "CREATE TABLE IF NOT EXISTS userheadonstats ( \
                userid text, \
                opponentid text, \
                wins counter, \
                losses counter, \
                draws counter, \
                surrenders counter, \
                PRIMARY KEY (userid, opponentid) \
                )"

        self.session.execute(userheadonstats)

        usergames = "CREATE TABLE IF NOT EXISTS usergames ( \
                userid text, \
                opponentid text, \
                gamecode uuid, \
                gamedate timeuuid, \
                status text, \
                ispublic boolean, \
                PRIMARY KEY (userid, gamedate, opponentid, gamecode)) \
                WITH CLUSTERING ORDER BY (gamedate DESC, opponentid ASC, gamecode ASC)"

        self.session.execute(usergames)

        indexstatususergames = "CREATE INDEX IF NOT EXISTS indexstatususergames \
                ON usergames(status)"

        self.session.execute(indexstatususergames)

        indexispublicusergames = "CREATE INDEX IF NOT EXISTS indexispublicusergames \
                ON usergames(ispublic)"

        self.session.execute(indexispublicusergames)


    def generateNewGame(self, boardState, userid=None, opponentid=None, ispublic=True):
        gamecode = uuid1()
        print(f'Generating New Game Before: userid: {userid}, opponentid: {opponentid}, ispublic: {ispublic}')
        if userid is None:
                userid = userid_generator()             # Only if user is not logged in
        if opponentid is None:
                opponentid = userid_generator()         # Only if user is not logged in
        print(f'Generating New Game After: userid: {userid}, opponentid: {opponentid}, ispublic: {ispublic}')
        curdate     = datetime.now()
        strcurdate  = curdate.strftime("%Y-%m-%d %H:%M:%S")
        board       = deepcopy(boardState)
        status      = 'New' if ispublic else 'Pending'
        insertChessGame = f"INSERT INTO chessgame ( \
                gamecode, gamedate, \
                gameturn, userid, opponentid, isactive, ispublic, starttime, status) VALUES ( \
                {gamecode}, now(), 'W', '{userid}', '{opponentid}', true, {ispublic}, '{strcurdate}', '{status}');"

        insertUserGameUser = f"INSERT INTO usergames (\
                userid, opponentid, gamedate, gamecode, status, ispublic) VALUES (\
                '{userid}', '{opponentid}', now(), {gamecode}, '{status}', {ispublic} \
                );"

        insertUserGameOpponent = f"INSERT INTO usergames (\
                userid, gamedate, opponentid, gamecode, status, ispublic) VALUES (\
                '{opponentid}', now(), '{userid}', {gamecode}, '{status}', {ispublic} \
                );"

        insertBoardState = f"INSERT INTO boardstate (\
                gamecode, movetime, boardState) VALUES (\
                {gamecode}, now(), {boardState}\
                );"

        insertBoardState = self.jsonifyMap(insertBoardState)

        updateGameStats = f"UPDATE gamestats SET \
                totalblackmoves = totalblackmoves + 0, \
                totalwhitemoves = totalwhitemoves + 0, \
                regeneratedblackrooks = regeneratedblackrooks + 2, \
                regeneratedblackkinghts = regeneratedblackkinghts + 2, \
                regeneratedblackbishops = regeneratedblackbishops + 2, \
                regeneratedblackqueens = regeneratedblackqueens + 0, \
                regeneratedwhiterooks = regeneratedwhiterooks + 2, \
                regeneratedwhitekinghts = regeneratedwhitekinghts + 2, \
                regeneratedwhitebishops = regeneratedwhitebishops + 2, \
                regeneratedwhitequeens = regeneratedwhitequeens + 0 \
                where gamecode = {gamecode};"


        batch = BatchStatement()
        batch.add(insertChessGame)
        batch.add(insertUserGameUser)
        batch.add(insertUserGameOpponent)
        batch.add(insertBoardState)
        self.session.execute(batch)
        self.session.execute(updateGameStats)
        return (str(gamecode), userid, opponentid)

    def jsonifyMap(self, boardState):
        boardState = boardState.replace("'curpos'", "curpos").replace("'posspos'", "posspos")
        boardState = boardState.replace("'moved'", "moved").replace("'score'", "score")
        boardState = boardState.replace("'range'", "range").replace("set()", "{}")
        boardState = boardState.replace("SortedSet([", "{").replace("])", "}")
        boardState = boardState.replace("'killable'", "killable")
        return boardState

    def loadGameInformation(self, gamecode):
        gamecode = UUID(gamecode)
        selectChessGame = f"SELECT gameturn, userid, opponentid, isactive, ispublic, status, wonby from chessgame \
                where gamecode = {gamecode};"

        rowsChessGame = self.session.execute(selectChessGame)
        return rowsChessGame.one()

    def loadBoardState(self, gamecode):
        gamecode = UUID(gamecode)
        selectBoardState = f"SELECT boardstate from boardstate \
                where gamecode = {gamecode} LIMIT 1;"

        rowsBoardState = self.session.execute(selectBoardState)
        return rowsBoardState.one()

    def loadGameMoves(self, gamecode):
        gamecode = UUID(gamecode)
        selectMoves = SimpleStatement(f"SELECT piece, prevloc, newloc, piececut, replaced from boardstate \
                where gamecode = {gamecode};", consistency_level=ConsistencyLevel.QUORUM)
        
        rowsMoves = self.session.execute(selectMoves)
        return rowsMoves

    def saveGameInformation(self, listPiece, gamecode, boardState, request):
        move = request.form['move']
        cut = request.form['cut']
        replaced = request.form['replaced']

        i = int(request.form['i'])
        j = int(request.form['j'])

        whoMoved = move[0]
        updatePreviousMove = 'previousblackmove = ' if whoMoved == 'B' else 'previouswhitemove = '
        updatePreviousMove = updatePreviousMove + f'{(i, j)}'

        updateGameTurn = listPiece['whoToMove']
        updateGameTurn = f"gameturn = '{updateGameTurn}'"

        updateIsActive = ""
        updateWonBy = ""

        status = 'In Progress'
        wonby = ''
        if listPiece['status'] in ('Checkmate', 'Mate'):
            status = listPiece['status']
            updateIsActive = "isActive = False, "
            if listPiece['status'] == 'Checkmate':
                wonby = 'Black' if whoMoved == 'B' else 'White'
            else:
                wonby = 'Black' if whoMoved == 'W' else 'White'
            updateWonBy = f"wonby = '{wonby}', "
        updateStatus = f"status = '{status}'"

        updateTotalMoves = 'totalblackmoves = totalblackmoves + 1' if whoMoved == 'B' else 'totalwhitemoves = totalwhitemoves + 1'

        insertBoardState = f"INSERT INTO boardstate ( \
                gamecode, movetime, boardState, piece, prevloc, newloc, piececut, replaced) VALUES ( \
                {gamecode}, now(), {boardState}, '{move}', {listPiece['prevloc']}, {(i, j)}, '{cut}', '{replaced}') \
                ;"
        insertBoardState = self.jsonifyMap(insertBoardState)

        updateChessGame = f"UPDATE chessgame SET \
                {updatePreviousMove}, \
                {updateGameTurn}, \
                {updateIsActive} \
                {updateWonBy} \
                {updateStatus} \
                WHERE gamecode = {gamecode} \
                ;"

        updateGameStats = f"UPDATE gamestats SET \
                {updateTotalMoves} \
                WHERE gamecode = {gamecode} \
                ;"

        batch = BatchStatement()
        batch.add(insertBoardState)
        batch.add(updateChessGame)
        self.session.execute(batch)
        self.session.execute(updateGameStats)
        return (status, wonby)

    def loadGamesList(self, pagelimit, userid=None, page=1, pending=False):
        directionmark = {
            'previous':'>', 
            'next':'<'
        }
        restrictTo = f"WHERE userid = '{userid}'" if userid is not None else "WHERE ispublic=True"
        restrictToStatus = ""
        if userid is not None:
            restrictToStatus = " AND status IN ('Pending')" if pending else ''
        selectUserGames = f"SELECT opponentid, gamecode, gamedate, status from usergames \
                {restrictTo} \
                {restrictToStatus} "
        print(selectUserGames)
        userGames = self.session.execute(selectUserGames)
        userGames = userGames.current_rows
        totalRecords = 0 if userGames is None else len(userGames)
        if totalRecords > pagelimit:
            startIndex = (page - 1) * pagelimit + 1
            endIndex = page * pagelimit + 1
            print(f'startIndex: {startIndex}, endIndex: {endIndex}')
            userGames = userGames[startIndex:endIndex]
        print(f'totalRecords: {totalRecords}, pagelimit: {pagelimit}')
        gamesList = [[game.opponentid, str(game.gamecode), game.status, str(game.gamedate)] for game in userGames]
        print(f'Games List: {gamesList}')
        return gamesList, totalRecords

    def getUserStats(self, userid=None):
        restrictTo = f"WHERE userid = '{userid}'" if userid is not None else ''
        selectUserStats = f"SELECT wins, losses, draws, surrenders from userstats \
            {restrictTo};"
        userStats = self.session.execute(selectUserStats)
        return userStats.one()

    def setGameStatus(self, gamecode, result, userid=None, opponentid=None, isactive=True, strEndDateTime=None):
        endTime = ""
        if strEndDateTime is not None:
            endTime = f"endtime = '{strEndDateTime}',"
        updateGameStatus = f"UPDATE chessgame SET \
            status='{result}', \
            {endTime} \
            isactive = {isactive} \
            WHERE gamecode = {UUID(gamecode)};"

        print(updateGameStatus)
        updateUserGameStatus = f"UPDATE usergames SET \
                status = '{result}' \
                WHERE userid = '{userid}' AND \
                opponentid = '{opponentid}' AND \
                gamecode = {UUID(gamecode)};"

        print(updateUserGameStatus)
        updateOpponentGameStatus = f"UPDATE usergames SET \
                status = '{result}' \
                WHERE userid = '{opponentid}' AND \
                opponentid = '{userid}' AND \
                gamecode = {UUID(gamecode)};"
        print(updateOpponentGameStatus)

        batch = BatchStatement()
        batch.add(updateGameStatus)
        batch.add(updateUserGameStatus)
        batch.add(updateOpponentGameStatus)
        self.session.execute(batch)

    def updateGameDetails(self, userid, opponentid, gamecode, result=None):
        if result is not None:
            endDateTime = datetime.now()
            strEndDateTime = endDateTime.strftime("%Y-%m-%d %H:%M:%S")

            self.setGameStatus(gamecode, result, userid=userid, opponentid=opponentid, isactive=False, strEndDateTime=strEndDateTime)

            if result == "draw":
                userResultCol = "draws"
                opponentResultCol = "draws"
            elif result == "win":
                userResultCol = "wins"
                opponentResultCol = "losses"
            elif result == "lost":
                userResultCol = "losses"
                opponentResultCol = "wins"
            else:
                userResultCol = "surrenders"
                opponentResultCol = "wins"

            updateUserStats = f"UPDATE userstats SET \
                {userResultCol} = {userResultCol} + 1 \
                WHERE userid = '{userid}' \
                ;"

            updateOpponentStats = f"UPDATE userstats SET \
                {opponentResultCol} = {opponentResultCol} + 1 \
                WHERE userid = '{opponentid}' \
                ;"

            updateUserHeadOnStats = f"UPDATE userheadonstats SET \
                {userResultCol} = {userResultCol} + 1 \
                WHERE userid = '{userid}' AND \
                opponentid = '{opponentid}' \
                ;"

            updateOpponentHeadOnStats = f"UPDATE userheadonstats SET \
                {opponentResultCol} = {opponentResultCol} + 1 \
                WHERE userid = '{opponentid}' AND \
                opponentid = '{userid}' \
                ;"

        self.session.execute(updateUserStats)
        self.session.execute(updateOpponentStats)
        self.session.execute(updateUserHeadOnStats)
        self.session.execute(updateOpponentHeadOnStats)

    def getRegenerationCounter(self, piece, gamecode):
        pieceColor = "white" if piece[0] == "W" else "black"
        pieceTypes = {"R":"rooks", "K":"knights", "B":"bishops", "Q":"queens"}
        pieceType = pieceTypes[piece[1]]

        columnname = f"regenerated{pieceColor+pieceType}"

        selectRegenerationCounter = f"SELECT {columnname} FROM gamestats \
            WHERE gamecode = {UUID(gamecode)};"

        selectedCounter = self.session.execute(selectRegenerationCounter)
        counter = selectedCounter.one()
        return counter[0]

    def isUserAuthenticated(self, request):
        user=request.form['username']
        password=request.form['password']

        selectUserDetails = f"SELECT userid, password, friends FROM users \
            WHERE userid='{user}';"

        userDetails = self.session.execute(selectUserDetails)
        userDetails = userDetails.one()
        if userDetails is None:
            return "Invalid Credentials!"
        if user == userDetails.userid and password == userDetails.password:
            return userDetails
        else:
            return "Invalid Credentials!"

    def isValidUser(self, user):
        selectUserDetails = f"SELECT userid FROM users \
            WHERE userid='{user}';"

        userDetails = self.session.execute(selectUserDetails)
        userDetails = userDetails.one()
        if userDetails is None:
            return "Invalid User!"
        if user == userDetails.userid:
            return "valid"
        else:
            return "Invalid User!"

    def signUpUser(self, request):
        user=request.form['username']
        password=request.form['password']
        email=request.form['email']

        selectUserID = f"SELECT userid FROM users \
            WHERE userid='{user}';"

        selectEmail = f"SELECT email FROM mvemailusers \
            WHERE email='{email}';"

        userIDDetails = None
        userEmail = None
        try:
            userIDDetails = self.session.execute(selectUserID)
            userIDDetails = userIDDetails.one()
            userEmail = self.session.execute(selectEmail)
            userEmail = userEmail.one()
        except Exception as e:
            print(f'Error while checking for users: {e}')
            pass

        if userIDDetails is None and userEmail is None:
            insertSignupDetails = f"INSERT INTO users \
                (userid, password, email) VALUES \
                ('{user}', '{password}', '{email}');"

            self.session.execute(insertSignupDetails)
            return True
        else:
            return "User Name or E-mail already registered!"

def userid_generator():
    allowed_chars = ascii_letters.replace("!", "")
    prefix = ''.join(choice(allowed_chars) for x in range(4))
    suffix = ''.join(choice(allowed_chars) for x in range(6))
    return prefix + "_" + suffix
