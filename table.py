import random
from player import Player
from itertools import combinations
class Card():
    def __init__(self,suit,value):
        self.suit=suit
        self.value=value
    def __repr__(self):
        suits={1:"Spades",2:"Hearts",3:"Diamonds",4:"Clubs"}
        values={14:"Ace",2:"Two",3:"Three",4:"Four",5:"Five",6:"Six",7:"Seven",8:"Eight",9:"Nine",10:"Ten",11:"Jack",12:"Queen",13:"King"}
        return values[self.value]+" of "+suits[self.suit]


class standardDeck(list):
    def __init__(self):
        suits=list(range(1,5))
        value=list(range(2,15))
        for i in suits:
            for j in value:
                self.append(Card(i,j))
    def shuffle(self):
        random.shuffle(self)
    def deal(self,location,num):
        for i in range(num):
            location.cards.append(self.pop())
    def show(self):
        for x in self:
            print(x)  
class Game():
    def __init__(self):
        self.playerList=[]
        self.deck=standardDeck()
        self.deck.shuffle()
        self.foldList=[]
        self.currentIndexPLayerFound=False
        self.cards=[]
        self.playersOnGame=[]
        self.gameOver=False
        self.bigBlind=Player()
        self.smallBlind=Player()
        self.firstActor=Player()
        self.dealer=Player()
        self.smallBlindAmount=5
        self.bigBlindAmount=10
        self.highestStake=10
        self.pot=0
        self.readyList=[]
        self.removeList=[]
        self.roundResumes=True
        self.dealtFlop=False
        self.highestScore=0
        self.playersWithHighestScore=[]
        self.winners=[]

    def possibleActions(self,player):
        player.allActions.clear()
        stakeDiff=self.highestStake-player.stake
        if player.chips>stakeDiff:
            if player.stake<self.highestStake:
                actions=["fold","call in exact","call and all-in","raise"]
            elif player.stake==self.highestStake:
                actions=["fold","check","raise","call and all-in"]
        elif player.chips==stakeDiff:
            actions=["fold","call and all-in"]
        else:
            actions=["fold","all-in"]
        player.allActions.extend(actions)
    def answer(self,player):
        if player.fold or player.all_in:
            return True
        stakeDiff=self.highestStake-player.stake
        if player.action=="fold":
            player.fold=True
            self.foldList.append(player)
            if len(self.foldList)==len(self.playersOnGame)-1:
                self.roundResumes=False
                for player in self.playersOnGame:
                    if not player.fold:
                        self.winners.append(player)
                        break
            return True
        if player.action=="call in exact":
            player.stake+=stakeDiff
            player.chips-=stakeDiff
            self.pot+=stakeDiff
            return True
        if player.action=="raise":
            raiseAmount=player.raiseAmount
            player.chips-=(stakeDiff+raiseAmount)
            player.stake+=(stakeDiff+raiseAmount)
            self.pot+=(stakeDiff+raiseAmount)
            self.highestStake+=raiseAmount
            print(self.pot,self.highestStake)
            self.readyList.clear()
            return True
        if player.action=="call and all-in":
            player.stake+=player.chips
            self.pot+=player.chips
            self.highestStake+=(player.chips-stakeDiff)
            player.chips=0
            player.all_in=True
            self.readyList.clear()
            return True
        if player.action=="check":
            print("in check")
            return True
        if player.action=="all-in":
            player.stake+=player.chips
            self.pot+=player.chips
            player.chips=0
            player.all_in=True
            return True


    def setAttributes(self,players):
        index=0
        self.dealer=players[index]
        self.dealer.attributes.append("dealer")
        index+=1
        index%=len(players)
        self.smallBlind=players[index]
        self.smallBlind.attributes.append("small blind")
        index+=1
        index%=len(players)
        self.bigBlind=players[index]
        self.bigBlind.attributes.append("big blind")
        index+=1
        index%=len(players)
        self.firstActor=players[index]
        self.firstActor.attributes.append("first actor")
        players.append(players.pop(0))
    def initialize(self):
        self.roundResumes=True
        self.smallBlind.chips-=self.smallBlindAmount
        self.smallBlind.stake+=self.smallBlindAmount
        self.bigBlind.chips-=self.bigBlindAmount
        self.bigBlind.stake+=self.bigBlindAmount
        self.pot+=self.smallBlindAmount+self.bigBlindAmount
        # self.askPlayers()

    def dealHole(self):
        for player in self.playersOnGame:
            self.deck.deal(player,2)
        self.initialize()
            
    def dealFlop(self):
        self.deck.deal(self,3)
        self.dealtFlop=True
    def dealTurn(self):
        self.deck.deal(self,1)
    def dealRiver(self):
        self.deck.deal(self,1)
    def checkHand(self,player):
        totalCards=self.cards+player.cards
        totalCombination=list(combinations(totalCards,5))
        for fiveCards in totalCombination:
            suits=[]
            values=[]
            for card in fiveCards:
                suits.append(card.suit)
                values.append(card.value)
            suits.sort(reverse=True)
            values.sort(reverse=True)
            numberOfDifferentSuits=len(list(set(suits)))
            if numberOfDifferentSuits==1:
                if 14 in values and 10 in values and 11 in values and 12 in values and 13 in values:
                    player.handScore=10
                    player.hand="Royal Flush"
                    player.winningSuits.clear()
                    player.winningValues.clear()
                    player.winningSuits.extend(suits)
                    player.winningValues.extend(values)
                    continue
                else:
                    straightFlush=True
                    prevValue=None
                    for i in values:
                        if prevValue is None:
                            prevValue=i
                        elif prevValue+1==i:
                            prevValue=i
                        else:
                            straightFlush=False
                            break
                    if straightFlush:
                        if player.handScore<9:
                            player.handScore=9
                            player.hand="Straight Flush"
                            player.winningSuits.clear()
                            player.winningValues.clear()
                            player.winningSuits.extend(suits)
                            player.winningValues.extend(values)
                        continue
                if player.handScore<=6:
                    if player.handScore<6:
                        player.handScore=6
                        player.hand="Flush"   
                        player.winningSuits.clear()
                        player.winningValues.clear()
                        player.winningSuits.extend(suits)
                        player.winningValues.extend(values)  
                    else:
                        if player.winningValues<values:
                            player.winningSuits.clear()
                            player.winningValues.clear()
                            player.winningSuits.append(suits)
                            player.winningValues.append(values)
                continue
            elif len(set(values))==2:
                valueOccurence={}
                for i in values:
                    if not valueOccurence:
                        valueOccurence[i]=1
                    else:
                        if i in valueOccurence:
                            valueOccurence[i]+=1
                        else:
                            otherCard=i
                for i in valueOccurence:
                    if valueOccurence[i]==1 or valueOccurence[i]==4:
                        if valueOccurence[i]==1:
                            kickerCard=i
                            highCard=otherCard
                        else:
                            kickerCard=otherCard
                            highCard=i
                        if player.handScore<8 or (player.handScore==8 and (player.kicker[0]<kickerCard)):
                            player.handScore=8
                            player.hand="4-of-a-kind"
                            player.winningSuits.clear()
                            player.winningValues.clear()
                            player.kicker.clear()
                            player.kicker.append(kickerCard)
                            player.highCard=highCard
                            player.winningSuits.extend(suits)
                            player.winningValues.extend(values)

                        continue
                    else:
                        if valueOccurence[i]==2:
                            kickerCard=i
                            highCard=otherCard
                        else:
                            kickerCard=otherCard
                            highCard=i
                        if player.handScore<7 or (player.handScore==7 and (player.kicker[0]<kickerCard)):
                            player.handScore=7
                            player.hand="full house"
                            player.winningSuits.clear()
                            player.winningValues.clear()
                            player.kicker.clear()
                            player.kicker.append(kickerCard)
                            player.highCard=highCard
                            player.winningSuits.extend(suits)
                            player.winningValues.extend(values)
                        continue
            elif len(set(values))==3:
                valueOccurence={}
                for i in values:
                    if i in valueOccurence:
                        valueOccurence[i]+=1
                    else:
                        valueOccurence[i]=1
                found=False
                kickerCards=[]
                for i in valueOccurence:
                    if valueOccurence[i]==3:
                        found=True
                        highCard=i
                        for j in valueOccurence:
                            if valueOccurence[j]!=3:
                                kickerCards.append(j)
                        break
                if found:
                    kickerCards.sort(reverse=True)
                    if player.handScore<4 :
                        player.handScore=4
                        player.hand="3-of-a-kind"
                        player.winningSuits.clear()
                        player.winningValues.clear()
                        player.kicker.clear()
                        player.highCard=highCard
                        player.kicker.extend(kickerCards)
                        player.winningSuits.extend(suits)
                        player.winningValues.extend(values)
                    elif player.handScore==4:
                        if player.highCard>highCard:
                            continue
                        elif player.highCard<highCard:
                            player.winningSuits.clear()
                            player.winningValues.clear()
                            player.kicker.clear()
                            player.kicker.extend(kickerCards)
                            player.highCard=highCard
                            player.winningSuits.extend(suits)
                            player.winningValues.extend(values)  
                            continue
                        else:
                            if player.kicker<kickerCards:
                                player.winningSuits.clear()
                                player.winningValues.clear()
                                player.kicker.clear()
                                player.kicker.extend(kickerCards)
                                player.highCard=highCard
                                player.winningSuits.extend(suits)
                                player.winningValues.extend(values)
                    continue
                else:
                    setOfPairs=[]
                    for i in valueOccurence:
                        if valueOccurence[i]==2:
                            setOfPairs.append(i)
                        else:
                            kickerCard=i
                    setOfPairs.sort(reverse=True)
                    if player.handScore<3:
                        player.handScore=3
                        player.hand="two pairs"
                        player.winningSuits.clear()
                        player.winningValues.clear()
                        player.kicker.clear()
                        player.winningSuits.extend(suits)
                        player.winningValues.extend(values)
                        player.pair.clear()
                        player.pair.extend(setOfPairs)
                        player.kicker.append(kickerCard)
                    elif player.handScore==3:
                        if player.pair<setOfPairs:
                            player.pair.clear()
                            player.pair.extend(setOfPairs)
                            player.kicker.clear()
                            player.kicker.append(kickerCard)
                            player.winningSuits.clear()
                            player.winningValues.clear()
                            player.winningSuits.extend(suits)
                            player.winningValues.extend(values)      
                        elif player.pair==setOfPairs:                   
                            if kickerCard>player.kicker[0]:
                                player.pair.clear()
                                player.pair.extend(setOfPairs)
                                player.kicker.clear()
                                player.kicker.append(kickerCard)
                                player.winningSuits.clear()
                                player.winningValues.clear()
                                player.winningSuits.extend(suits)
                                player.winningValues.extend(values)
                    continue
            elif len(set(values))==4:
                valueOccurence={}
                for i in values:
                    if i in valueOccurence:
                        valueOccurence[i]+=1
                    else:
                        valueOccurence[i]=1
                kickerCards=[]
                for i in valueOccurence:
                    if valueOccurence[i]==2:
                        pair=i
                    else:
                        kickerCards.append(i)
                    kickerCards.sort(reverse=True)
                if player.handScore<2:
                    player.handScore=2
                    player.hand="one pair"
                    player.winningSuits.clear()
                    player.winningValues.clear()
                    player.kicker.clear()
                    player.kicker.extend(kickerCards)
                    player.pair.clear()
                    player.pair.append(pair)
                    player.winningSuits.extend(suits)
                    player.winningValues.extend(values)
                if player.handScore==2:
                    if pair>player.pair[0]:
                        player.winningSuits.clear()
                        player.winningValues.clear()
                        player.kicker.clear()
                        player.kicker.extend(kickerCards)
                        player.pair.clear()
                        player.pair.append(pair)
                        player.winningSuits.extend(suits)
                        player.winningValues.extend(values)
                        continue
                    elif pair==player.pair[0]:
                        if player.kicker<kickerCards:
                            player.winningSuits.clear()
                            player.winningValues.clear()
                            player.kicker.clear()
                            player.kicker.extend(kickerCards)
                            player.pair.clear()
                            player.pair.append(pair)
                            player.winningSuits.extend(suits)
                            player.winningValues.extend(values) 
                continue
            prevValue=None
            straightFound=True
            for i in values:
                if prevValue  is None:
                    prevValue=i
                elif prevValue+1==i:
                    continue
                else:
                    straightFound=False
                    break
            if straightFound:
                if player.handScore<=5:
                    player.handScore=5
                    player.hand="straight"
                    player.winningSuits.clear()
                    player.winningValues.clear()
                    player.winningSuits.extend(suits)
                    player.winningValues.extend(values)
                else:
                    if player.winningValues<values:
                        player.winningSuits.clear()
                        player.winningValues.clear()
                        player.winningSuits.extend(suits)
                        player.winningValues.extend(values)                    
                continue
            if player.handScore<=1:
                if player.handScore==0:
                    player.handScore=1
                    player.hand="high card"
                    player.winningSuits.clear()
                    player.winningValues.clear()
                    player.winningSuits.extend(suits)
                    player.winningValues.extend(values)
                else:
                    if player.winningValues<values:
                        player.winningSuits.clear()
                        player.winningValues.clear()
                        player.winningSuits.extend(suits)
                        player.winningValues.extend(values)
            
    def findWinner(self):
        currentHighestPlayer=None
        possibleWinners=[]
        for player in self.playersWithHighestScore:
            if player.handScore==10:
                break
            elif player.handScore==9:
                if currentHighestPlayer is None:
                    currentHighestPlayer=player
                    self.winners.append(player)
                elif currentHighestPlayer.winningValues[-1]<player.winningValues[-1]:
                    currentHighestPlayer=player
                    self.winners.clear()
                    self.winners.append(player)
                elif currentHighestPlayer.winningValues[-1]==player.winningValues[-1]:
                    self.winners.append(player)
                else:
                    pass
            elif player.handScore==8:
                if currentHighestPlayer is None:
                    currentHighestPlayer=player
                    possibleWinners.append(player)
                else:
                    if currentHighestPlayer.highCard<player.highCard:
                        currentHighestPlayer=player
                        possibleWinners.clear()
                        possibleWinners.append(player)
            elif player.handScore==7:
                if currentHighestPlayer is None:
                    currentHighestPlayer=player
                    possibleWinners.append(player)
                else:
                    if currentHighestPlayer.highCard<player.highCard:
                        currentHighestPlayer=player
                        possibleWinners.clear()
                        possibleWinners.append(player)
                    elif currentHighestPlayer.highCard==player.highCard:
                        if currentHighestPlayer.kicker[0]<player.kicker[0]:
                            currentHighestPlayer=player
                            possibleWinners.clear()
                            possibleWinners.append(player)
                        elif currentHighestPlayer.kicker[0]==player.kicker[0]:
                            possibleWinners.append(player)
            elif player.handScore==6:
                if currentHighestPlayer is None:
                    currentHighestPlayer=player
                    possibleWinners.append(player)
                else:
                    if currentHighestPlayer.winningValues<player.winningValues:
                        currentHighestPlayer=player
                        possibleWinners.clear()
                        possibleWinners.append(player)
            elif player.handScore==5:
                if currentHighestPlayer is None:
                    currentHighestPlayer=player
                else:
                    if currentHighestPlayer.winningValues<=player.winningValues:
                        currentHighestPlayer=player
                        possibleWinners.clear()
                        possibleWinners.append(player)
            elif player.handScore==4:
                if currentHighestPlayer is None:
                    currentHighestPlayer=player
                    possibleWinners.append(player)
                else:
                    if currentHighestPlayer.highCard<player.highCard:
                        currentHighestPlayer=player
                        possibleWinners.clear()
                        possibleWinners.append(player)
                    elif currentHighestPlayer.highCard==player.highCard:
                        if currentHighestPlayer.kicker<player.kicker:
                            currentHighestPlayer=player
                            possibleWinners.clear()
                            possibleWinners.append(player)
                        if currentHighestPlayer.kicker==player.kicker:
                            possibleWinners.append(player)
            elif player.handScore==3:
                if currentHighestPlayer is None:
                    currentHighestPlayer=player
                    possibleWinners.append(player)
                else:
                    if currentHighestPlayer.pair<player.pair:
                        currentHighestPlayer=player
                        possibleWinners.clear()
                        possibleWinners.append(player)
                    elif currentHighestPlayer.pair==player.pair:
                        if currentHighestPlayer.kicker<player.kicker:
                            currentHighestPlayer=player
                            possibleWinners.clear()
                            possibleWinners.append(player)
                        elif currentHighestPlayer.kicker==player.kicker:
                            possibleWinners.append(player)
            elif player.handScore==2:
                if currentHighestPlayer is None:
                    currentHighestPlayer=player
                    possibleWinners.append(player)
                else:
                    if currentHighestPlayer.pair<player.pair or (currentHighestPlayer.pair==player.pair and currentHighestPlayer.kicker<player.kicker):
                        currentHighestPlayer=player
                        possibleWinners.clear()
                        possibleWinners.append(player)
                    elif currentHighestPlayer.pair==player.pair and currentHighestPlayer.kicker==player.kicker:
                        possibleWinners.append(player)
            elif player.handScore==1:
                if currentHighestPlayer is None:
                    currentHighestPlayer=player
                else:
                    if currentHighestPlayer.winningValues<=player.winningValues:
                        currentHighestPlayer=player
                        possibleWinners.clear()
                        possibleWinners.append(player)
        return possibleWinners

    def compute(self):
        playersOnBoard=[]
        listOfStakes=[]
        for player in self.playersOnGame:
            if player.fold:

                continue
            else:
                playersOnBoard.append(player)
                listOfStakes.append(player.stake)
                self.checkHand(player)
                if self.highestScore<player.handScore:
                    self.highestScore=player.handScore
                    self.playersWithHighestScore.clear()
                    self.playersWithHighestScore.append(player)
                elif self.highestScore==player.handScore:
                    self.playersWithHighestScore.append(player)
        if len(self.playersWithHighestScore)==1:
            for player in self.playersWithHighestScore:
                self.winners.append(player)
                player.winner=True
                if player.stake==self.highestStake:
                    player.chips+=self.pot
                else:
                    winningAmount=0
                    for player in playersOnBoard:
                        if player.stake>self.winners[0].stake:
                            winningAmount+=self.winners[0].stake
                            self.pot-=self.winners[0].stake
                            player.chips+=(player.stake-self.winners[0].stake)
                        if player.stake<=self.winners[0].stake:
                            winningAmount+=player.stake
                            self.pot-=player.stake
                    self.winners[0].chips+=winningAmount  
        else:
            possibleWinners=self.findWinner()
            if len(possibleWinners)==1:
                for player in possibleWinners:
                    self.winners.append(player)
                    player.winner=True
                    if player.stake==self.highestStake:
                        player.chips+=self.pot
                    else:
                        winningAmount=0
                        for player in playersOnBoard:
                            if player.stake<=self.winners[0].stake:
                                winningAmount+=player.stake
                                self.pot-=player.stake
                            elif player.stake>self.winners[0].stake:
                                winningAmount+=self.winners[0].stake
                                self.pot-=self.winners[0].stake
                                player.chips+=(player.stake-self.winners[0].stake)
                        self.winners[0].chips+=winningAmount
            else:
                eachAmount=self.pot//len(possibleWinners)
                print("The winners of this round are:")
                for player in possibleWinners:
                    player.chips+=eachAmount
                    self.winners.clear()
                    self.winners.append(player)
    def roundEnded(self):
        print("\nround ended\n")
        removeList=[]
        for player in self.playersOnGame:
            if player.chips<=0:
                removeList.append(player)
        self.removeList.extend(removeList)
    def clearBoard(self):
        for player in self.playersOnGame:
            player.pair.clear()
            player.highCard=None
            player.kicker.clear()
            player.stake=0
            player.cards.clear()
            player.fold=False
            player.all_in=False
            player.attributes.clear()
            player.action=None
            player.handScore=0
            player.hand=None
            player.winningSuits.clear()
            player.winningValues.clear()
            player.winner=False
        
        self.deck=standardDeck()
        self.deck.shuffle()
        self.foldList.clear()
        self.cards.clear()
        self.highestStake=self.bigBlindAmount
        self.pot=0
        self.readyList.clear()
        self.dealtFlop=False
        self.highestScore=0
        self.playersWithHighestScore.clear()

