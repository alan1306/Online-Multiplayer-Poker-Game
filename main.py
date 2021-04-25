from itertools import combinations
import random
import _pickle as pickle 
from client import Network

def main():
    server=Network()
    name=input(f"Enter the name of player:")
    playerId=server.connect(name)
    while True:
        try:
            data=server.client.recv(2048*4)
            game,player=pickle.loads(data)
        except:
            break
        if game.roundResumes:
            print(player.name,player.cards,player.attributes)
            if game.dealtFlop:
                print(f"\nGame cards are:{game.cards}\n")
            print(f"Chips remaining:{player.chips}")
            print(f"Current stake:{player.stake}")
            print(f"Current highest stake:{game.highestStake}")
            print(f"Total chips on pot:{game.pot}")
            print("Choose your action:")
            for i in range(len(player.allActions)):
                print(str(i+1)+" "+player.allActions[i])
            choice=int(input())
            if player.allActions[choice-1]=="raise":
                raiseAmount=int(input("How much to Raise:"))
                data="raise"+" "+str(raiseAmount)
            else:
                data=player.allActions[choice-1]
            data=str.encode(data)
            server.client.send(data)
        else:
            found=False
            print(f"the Game cards are:{game.cards}\n")
            print(f"your cards are:{player.cards}\n\n")
            for player in game.winners:
                if player.id==playerId:
                    print("congraluations you are the winner")
                    found=True
            if not found:
                print("sorry you are not the winner.\nThe winners are:")
                for player in game.winners:
                    print(player.name)
            if player.chips<=0:
                 print("\nSorry you are out of the game")
main()     
print("\nYou are disconnected from the server")       