from flask import Flask, render_template
from cassandra.cluster import Cluster

global session
KEYSPACENAME = 'docker'

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/newchess')
def newchess():
    global session
    session.execute(f"use {KEYSPACENAME};")
    boardstate = {'BR1':(0,0),'BK1':(0,1),'BB1':(0,2),'BQ':(0,3),
                'BX':(0,4),'BB2':(0,5),'BK2':(0,6),'BR2':(0,7),
                'BP1':(1,0),'BP2':(1,1),'BP3':(1,2),'BP4':(1,3),
                'BP5':(1,4),'BP6':(1,5),'BP7':(1,6),'BP8':(1,7),
                'WP1':(6,0),'WP2':(6,1),'WP3':(6,2),'WP4':(6,3),
                'WP5':(6,4),'WP6':(6,5),'WP7':(6,6),'WP8':(6,7),
                'WR1':(7,0),'WK1':(7,1),'WB1':(7,2),'WQ':(7,3),
                'WX':(7,4),'WB2':(7,5),'WK2':(7,6),'WR2':(7,7)}
    insert = f"INSERT INTO chessgame (gamecode, gamedate, boardstate, gameturn) VALUES (uuid(), now(), {boardstate}, 'W');"

    session.execute(insert)
    return render_template('board.html')

@app.route('/loadchess')
def loadchess():
    global session
    session.execute(f"use {KEYSPACENAME};")
    select = "SELECT gamecode from chessgame;"
    data = session.execute(select)
    return render_template('listgames.html', data=data)

if __name__ == '__main__':
    cluster = Cluster(['127.0.0.2', '127.0.0.3'])
    global session
    session = cluster.connect()
    keyspace = "CREATE KEYSPACE IF NOT EXISTS %s WITH replication = \
                {'class': 'NetworkTopologyStrategy', 'dc1': '1', 'dc2': '1'} \
                    AND durable_writes = true;"%(KEYSPACENAME, )
    #print (f'Keyspace: {keyspace}')
    session.execute(keyspace)

    #print(f"USE {KEYSPACENAME};")
    session.execute(f"USE {KEYSPACENAME};")

    table = "CREATE TABLE IF NOT EXISTS chessgame ( \
            gamecode uuid, \
            gamedate timeuuid, \
            boardstate map<text, tuple<int, int>>, \
            gameturn text STATIC, \
            PRIMARY KEY (gamecode, gamedate) )"

    #print(f"Table: {table};")
    session.execute(table)

    app.run()