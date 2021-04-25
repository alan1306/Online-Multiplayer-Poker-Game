class Player():
    def __init__(self,name=None,playerId=None):
        self.name=name
        self.id=playerId
        self.cards=[]
        self.chips=200
        self.fold=False
        self.all_in=False
        self.attributes=[]
        self.stake=0
        self.allActions=[]
        self.action=None
        self.handScore=0
        self.hand=None
        self.winningSuits=[]
        self.winningValues=[]
        self.kicker=[]
        self.highCard=None
        self.pair=[]
        self.winner=False
        self.raiseAmount=0
    def __repr__(self):
        return self.name

