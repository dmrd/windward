carrying = None
carried = None

def initialize(players):
    carrying = { player.guid : None for player in players }
    carried = { player.guid : set() for player in players }


def recordAbandon(limo, passenger):
    pass

def recordPickup(limo, passenger):
    pass

def recordDeliver(limo, passenger):
    pass