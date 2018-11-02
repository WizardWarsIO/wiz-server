from flask import Flask
from flask import request
from flask_socketio import SocketIO, emit, send
import threading

from client import *
import json

import gc
gc.enable()
import time

from datetime import datetime

client = Client()

playerNames = {}
avatars = {}
global sockets
sockets = {}

app = Flask(__name__, static_url_path='')
socketio = SocketIO(app)

game = None

class Socket:
    def __init__(self, sid):
        self.sid = sid
        self.connected = True

    def emit(self, event, data):
        socketio.emit(event, data, room=self.sid)


@socketio.on('connect')
def connect():
    pass

def printPlayerNames():
    names = []
    for k,v in playerNames.iteritems():
        names.append(v)
    print "Player names" + str(names)

def allAvatars():
    avs = []
    for k,v in avatars.iteritems():
        avs.append(v)
    return avs

def printLog(playerName):
    print playerName + ' joined at ' + str(datetime.now()) + '.'
    printPlayerNames()

@socketio.on('joingame')
def joingame(message):
    pid = request.sid
    if pid in sockets.keys():
        return
    playerName = message['name']
    playerName = (playerName[:22]) if len(playerName) > 22 else playerName
    ns = Socket(pid)
    ns.playerName = playerName
    sockets[pid] = ns
    playerNames[pid] = playerName
    avatar = client.newAvatar(playerName, pid)
    playerName = avatar.name
    avatars[pid] = avatar
    printLog(playerName)
    global game
    if game:
        game.sendIn([avatar])
    else:
        game = client.makeGame({'gameID':1, 'avatarList':allAvatars()})

    styleGuide = client.styleGuide
    sockets[pid].emit('foo', {'playerID':pid, 'styleGuide':styleGuide})

@socketio.on('masterloop')
def masterloop():
    global game
    if not game:
        print "No game, returning"
        return
    game.msg('loop', 1)
    gc.collect()
    sidsToRemove = []
    firstPlace = game.firstPlace()

    global sockets
    if game.isFinished:
        for playerID in sockets.keys():
            playerInfo = game.getPlayerInfo(playerID)
            sockets[playerID].emit('playerinfo', {'data':playerInfo})
        game.components = []
        x = 0
        game = None
        removePlayerData(sockets.keys())
        sockets = {}
        global playerNames
        playerNames = {}
        global avatars
        avatars = {}
        print("Making new game")
        gc.collect()
        game = client.makeGame({'gameID':1, 'avatarList':[]})
        gc.collect()
        return
    for sid in sockets:
        playerID = sid
        playerInfo = game.getPlayerInfo(playerID)
        if 'error' in playerInfo.keys():
            sidsToRemove.append(sid)
            sockets[sid].emit('gameover', {'game':'over'})
        else:
            sockets[sid].emit('playerinfo', {'data':playerInfo})
    removePlayerData(sidsToRemove)

def removePlayerData(sidsToRemove):
    for sid in sidsToRemove:
        sockets[sid].emit('gameover', {'game':'over'})
        print "Removing player" + playerNames[sid]
        del sockets[sid]
        del avatars[sid]
        del playerNames[sid]
        printPlayerNames()


@app.route('/startgame')
def startGame():
    global game
    client.makeGame({'gameID':1, 'level':1, 'avatarList':allAvatars()})
    game = client.getGame(1)
    return 'Game started'

@app.route("/")
def hello():
    return app.send_static_file('index.html')

@socketio.on('heartbeat')
def heartbeat(message):
    pass

@socketio.on('input')
def input_response(message):
    if not game:
        return
    move = message
    moveDirs = {0:[0, 0], 1:[-1, 1], 2:[0, 1], 3:[1,1], 4:[-1, 0], 5:[0,0], 6:[1, 0], 7:[-1,-1], 8:[0, -1], 9:[1,-1]}
    playerID = move['playerID']
    intentType = move['type']
    itemNum = move['num']
    direction = move['dir']
    moveTo = moveDirs[direction]
    game.msg('input', {'name': playerID, 'intent':{'type':intentType, 'item':itemNum, 'direction':moveTo}})


def set_interval(func, sec):
    def func_wrapper():
        set_interval(func, sec)
        func()
    t = threading.Timer(sec, func_wrapper)
    t.start()
    return t

set_interval(masterloop, 1)
