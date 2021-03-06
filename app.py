from flask import Flask, render_template, request, session, flash, redirect, url_for
from flask.json import jsonify
from os import urandom
import flask_login

from ChessManagement import ChessManagement
from DatabaseManagement import DatabaseManagement

objChess = None
db = None
PAGE_LIMIT = 10

app = Flask(__name__)

@app.route('/')
def index():
    if session.get("logged_in", None) is True:
        return redirect(url_for('listgames', page='1'))
    elif session.get("error", None) is not None:
        return render_template("login.html", error = session.get("error"))
    else:
        return render_template("login.html")

@app.route('/signuplogin')
def signuplogin():
    return render_template('login.html')

@app.route('/signup', methods=['POST'])
def signup():
    global db
    output = db.signUpUser(request)
    if type(output) == str:
        return render_template('login.html', output=output, type="fail")
    else:
        return render_template('login.html', output = "User registered successfully!", type="success")

@app.route('/login', methods=['POST'])
def login():
    global db
    user=request.form['username']
    output = db.isUserAuthenticated(request)
    print(f'output: {output}')
    if type(output) == str:
        print(f"Error: {output}")
        session['error'] = output
    else:
        session['logged_in'] = True
        session['username'] = user
        session['friends'] = output.friends or ''
    # if user=='admin' and password=='password':
    #     session['logged_in'] = True
    #     session['username'] = user
    # else:
    #     flash("Wrong Password")
    return index()

@app.route('/logout')
def logout():
    session["logged_in"] = False
    del session['username']
    del session['friends']

    return redirect(url_for('signuplogin'))

@app.route('/invite', methods=['POST'])
def invite():
    print(f"session.get('logged_in', None): {session.get('logged_in', None)}")
    if session.get("logged_in", None) is True:
        global db
        user=request.form['inviteuser']
        print(f'user: {user}')
        output = db.isValidUser(user)
        print(f'output: {output}')
        listoutput = {}
        if output != 'valid':
            listoutput['inviteerror'] = output
            return listoutput
        else:
            global objChess
            objChess = ChessManagement()
            print(f"User: {session['username']}, Opponent: {user}")
            gamecode = createNewGame(userid=session['username'], opponentid=user, ispublic=False)
            listoutput['invitesuccess'] = "Invite sent!"
            return listoutput
    else:
        print("Redirecting for login!")
        return redirect(url_for('signuplogin'))


@app.route('/boardstate', methods=['POST'])
def boardstate():
    gc = request.form['gc']
    if gc is None or gc == '':
        return None
    else:
        global objChess
        global gameInformation

        objChess = ChessManagement()
        gameInformation = db.loadGameInformation(gc)
        if not gameInformation.ispublic and session.get('username', None) is None:
            return "login_required"
        else:
            boardState = db.loadBoardState(gc)
            gameMoves = db.loadGameMoves(gc)

            moves = []
            for i, move in enumerate(gameMoves):
                if move.piece is not None:
                    moves.append({
                        'move':move.piece, 
                        'prevloc':list(move.prevloc), 
                        'newloc':list(move.newloc), 
                        'piececut':move.piececut,
                        'replaced': move.replaced or ""
                    })

            boardState = objChess.createBoardState(boardState)

            session['opponentid'] = gameInformation.opponentid

            objChess.listpiece["boardState"] = boardState
            objChess.listpiece["whoToMove"] = gameInformation.gameturn
            objChess.listpiece["userid"] = gameInformation.userid
            objChess.listpiece["opponentid"] = gameInformation.opponentid
            objChess.listpiece["isactive"] = str(gameInformation.isactive)
            objChess.listpiece["moves"] = moves
            objChess.listpiece["status"] = gameInformation.status or ""
            objChess.listpiece["wonby"] = gameInformation.wonby or ""
            return objChess.listpiece

@app.route('/board/<gc>')
def board(gc):
    global objChess
    global db
    if gc == 'new':
        objChess = ChessManagement()
        gamecode = createNewGame()
        return redirect(url_for('board', gc=gamecode))
    else:
        objChess = ChessManagement()
        gameInformation = db.loadGameInformation(gc)
        if not gameInformation.ispublic and session.get('username', None) is None:
            print("Redirecting for login!")
            return redirect(url_for('signuplogin'))
        else:
            boardState = db.loadBoardState(gc)
            gameMoves = db.loadGameMoves(gc)

            moves = []
            for i, move in enumerate(gameMoves):
                if move.piece is not None:
                    moves.append({
                        'move':move.piece, 
                        'prevloc':list(move.prevloc), 
                        'newloc':list(move.newloc), 
                        'piececut':move.piececut,
                        'replaced': move.replaced or ""
                    })

            boardState = objChess.createBoardState(boardState)

            session['opponentid'] = gameInformation.opponentid

            objChess.listpiece["boardState"] = boardState
            objChess.listpiece["whoToMove"] = gameInformation.gameturn
            objChess.listpiece["userid"] = gameInformation.userid
            objChess.listpiece["opponentid"] = gameInformation.opponentid
            objChess.listpiece["isactive"] = str(gameInformation.isactive)
            objChess.listpiece["moves"] = moves
            objChess.listpiece["status"] = gameInformation.status or ""
            objChess.listpiece["wonby"] = gameInformation.wonby or ""
            return render_template('board.html',data=objChess.listpiece, logged=session.get("logged_in"), user=session.get("username"))

@app.route('/acceptinvite', methods=['POST'])
def acceptinvite():
    data = {}
    try:
        status = 'In Progress'
        gc=request.form['gc']
        if gc is not None and gc != '':
            db.setGameStatus(gc, "In Progress", userid=session.get('username'), opponentid=session.get('opponentid'))
            data['status'] = status
    except Exception as e:
        print(f"Error while setting status: {e}")
        data['status'] = f"Error while setting status. {e}"
    return data

@app.route('/listgames/<page>')
def listgames(page='1'):
    if session.get("logged_in", None) is True:
        global objChess
        global db
        gamesList, totalRecords = db.loadGamesList(PAGE_LIMIT, 
                                        page=int(page), 
                                        userid=session['username']) # pass session['username']

        userStatsResult = db.getUserStats(userid=session['username']) # pass session['username']

        userStats = [0,0,0,0]
        if userStatsResult is not None:
            userStats[0] = userStatsResult.wins or 0
            userStats[1] = userStatsResult.losses or 0
            userStats[2] = userStatsResult.draws or 0
            userStats[3] = userStatsResult.surrenders or 0

        return render_template(
            'listgames.html', 
            data=gamesList, 
            totalrecords=totalRecords,
            pagelimit=PAGE_LIMIT,
            userstats=userStats, 
            logged=session.get("logged_in"), 
            user=session.get("username")
        )
    else:
        return redirect(url_for('signuplogin'))

@app.route('/public/<page>')
def public(page='1'):
    global objChess
    global db
    gamesList, totalRecords = db.loadGamesList(PAGE_LIMIT, page=int(page))

    return render_template(
        'public.html', 
        data=gamesList, 
        totalrecords=totalRecords,
        pagelimit=PAGE_LIMIT,
        logged=session.get("logged_in"), 
        user=session.get("username")
    )

@app.route('/pending/<page>')
def pending(page='1'):
    if session.get("logged_in", None) is True:
        global objChess
        global db
        gamesList, totalRecords = db.loadGamesList(PAGE_LIMIT, userid=session['username'], page=int(page), pending=True)

        return render_template(
            'pending.html', 
            data=gamesList, 
            totalrecords=totalRecords,
            pagelimit=PAGE_LIMIT,
            logged=session.get("logged_in"), 
            user=session.get("username")
        )
    else:
        return redirect(url_for('signuplogin'))

@app.route('/showMoves', methods=['GET','POST'])
def showMoves():
    global objChess
    listpiece = objChess.showMoves(request)
    return listpiece

@app.route('/movePiece/<gc>', methods=['GET','POST'])
def movePiece(gc):
    global objChess
    global db
    replaced = request.form['replaced']
    counter = None
    if replaced != "":
        counter = db.getRegenerationCounter(replaced, gc)
    listpiece = objChess.movePiece(request, counter)
    listpiece['status'], listpiece['wonby'] = db.saveGameInformation(listpiece, gc, objChess.board, request)

    del listpiece['prevloc']
    return jsonify(listpiece)

@app.route("/drawresult", methods=['POST'])
def drawresult():
    global objChess
    global db
    gc=request.form['gc']
    userid=request.form["userid"]
    opponentid=request.form["opponentid"]
    db.updateGameDetails(userid, opponentid, gc, result="draw")
    return "draw"

@app.route("/surrenderresult", methods=['POST'])
def surrenderresult():
    global objChess
    global db
    gc=request.form['gc']
    userid=request.form["userid"]
    opponentid=request.form["opponentid"]
    db.updateGameDetails(userid, opponentid, gc, result="surrender")
    return "surrender"

def createNewGame(userid=None, opponentid=None, ispublic=True):
    global objChess
    boardState = objChess.createBoardState()
    board = objChess.getBoard()
    gamecode, userid, opponentid        = db.generateNewGame(board, userid=userid, opponentid=opponentid, ispublic=ispublic)
    objChess.listpiece["boardState"]    = boardState
    objChess.listpiece["whoToMove"]     = "W"
    objChess.listpiece["gamecode"]      = gamecode
    objChess.listpiece["userid"]        = userid
    objChess.listpiece["opponentid"]    = opponentid
    objChess.listpiece["isactive"]      = str(True)
    objChess.listpiece["ispublic"]      = ispublic
    return gamecode

if __name__ == '__main__':
    app.secret_key = urandom(128)
    db = DatabaseManagement()
    db.loadDatabase()
    # app.run()
    app.run(host="172.18.0.6")