import socket
from _thread import *
import _pickle as pickle
import sys
playerId=0
connections=0
playerList=[]
from player import Player
from table import Game
roundStarted=False
gameStarted=False
server='192.168.56.1'
port=5555
index=0
allConnections={}
allAddress={}
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
game=Game()
try:
    s.bind((server,port))
except socket.error as e:
    print(str(e))
    print("server could not connect")
s.listen()
print("waiting for connection,server started")
def setConnections():
    global connections
    for player in game.removeList:
        game.playerList.remove(player)
        if player.id in allConnections:
            conn=allConnections[player.id]
            conn.close()
            connections-=1
    if connections>=2:
        playGame()
    else:
        global roundStarted
        roundStarted=False
def askPlayers():
    index=game.playersOnGame.index(game.firstActor)
    game.readyList.clear()
    while True:
        currPlayer=game.playersOnGame[index]
        if currPlayer.id in allConnections:
            currConn=allConnections[currPlayer.id]
            game.possibleActions(currPlayer)
            print(game.pot,game.highestStake)
            if  currPlayer.fold or currPlayer.all_in:
                pass
            else:
                print("in if")
                currConn.send(pickle.dumps((game,currPlayer)))
                data=currConn.recv(1024)
                data=data.decode("utf-8")
                if data.split()[0]=="raise":
                    currPlayer.raiseAmount=int(data.split()[1])
                    currPlayer.action=data.split()[0]
                else:
                    currPlayer.action=data
                print(currPlayer.action,currPlayer.raiseAmount)
            playerReady=game.answer(currPlayer)
        if playerReady:
            game.readyList.append(currPlayer)
        if len(game.readyList)==len(game.playersOnGame) or not game.roundResumes:
            break
        index+=1
        index%=len(game.playersOnGame)
def declareWinner():    
    for player in game.playersOnGame:
        if player.id in allConnections:
            conn=allConnections[player.id]
            data=pickle.dumps((game,player))
            conn.send(data)
def playGame():
    game.playersOnGame=game.playerList[:]
    game.setAttributes(game.playersOnGame)
    game.dealHole()
    askPlayers()
    if game.roundResumes:
        game.dealFlop()
        askPlayers()
    if game.roundResumes:
        game.dealTurn()
        askPlayers()
    if game.roundResumes:
        game.dealRiver()
        askPlayers()
    if game.roundResumes:
        game.compute()
    game.roundResumes=False
    declareWinner()
    game.roundEnded()
    game.clearBoard()
    setConnections()
while True:
    conn,addr=s.accept()
    connections+=1
    allConnections[playerId]=conn
    allAddress[playerId]=addr
    data=conn.recv(1024)
    name=data.decode("utf-8")
    conn.send(str.encode(str(playerId)))
    print(f"{name} connected")
    player=Player(name,playerId)
    game.playerList.append(player)
    if connections>=2:
        if not roundStarted:
            roundStarted=True
            playGame()
    playerId+=1