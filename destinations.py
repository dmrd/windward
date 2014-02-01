import random as rand
import simpleAStar

def tripDistance(brain, start, dest):
    """ Return shortest path distance between start and dest """
    return len(simpleAStarcalculatePath(brain.gameMap, start, dest))


def totalTripDistance(brain, limo, passenger, needsCoffee=False):
    """ Calculate total distance from car->pickup->destination """

    # if the passenger is already in a limo, fuggedaboutit
    if passenger.car != None:
        return None

    bestCoffeeShop = None

    if needsCoffee:
        firstLeg = float('inf')
        for coffeeShop in brain.stores: # fix this
            distance = tripDistance(brain, limo.tilePosition, coffeeShop.busStop) + 
                        tripDistance(brain, coffeeShop.busStop, passenger.lobby)
            if distance < firstLeg:
                firstLeg = distance
                bestCoffeeShop = coffeeShop
    else:
        firstLeg = tripDistance(brain, limo.tilePosition, passenger.lobby)

    secondLeg = tripDistance(brain, passenger.lobby, passenger.destination)

    totalDistance = firstLeg + secondLeg

    return (totalDistance, bestCoffeeShop) # Placeholder

def getBestEnemyTarget(brain, enemyLimo):
    enemyTripDistances = [totalTripDistance(brain, enemyLimo, passenger) for passenger in brain.passengers]
    bestTarget = min(enemyTripDistances)
    pickupDistance = totalTripDistance(brain, enemyLimo.tilePosition, passenger.lobby)
    return (bestTarget, pickupDistance)

def rankPassengers(brain, needsCoffee=False):
    openPassengers = [passenger for passenger in brain.passengers if passenger.limo == None]
    tripDistances = [totalTripDistance(brain, brain.me.limo, passenger, needsCoffee) for passenger in openPassengers]
    pointsDelivered = [passenger.pointsDelivered for passenger in openPassengers]
    ordered = sorted(zip(pointsDelivered, tripDistances, passengers), key=lambda x: (-x[0], x[1]))
    unzipped = zip(*ordered)
    return zip(*ordered)[2] # Get passengers

def getOurBestPassenger(brain, needsCoffee=False):
    orderedPassengers = rankPassengers(brain, needsCoffee)
    enemyPassengers = [getBestEnemyTarget(brain, enemy) for enemy in brain.players if enemy != brain.me]
    pDistance = dict(enemyPassengers)
    candidates = []
    taken = []
    for passenger in orderedPassengers:
        if passenger in pDistance:
            pickupDist = tripDistance(brain, brain.me.limo.tilePosition, passenger.lobby)
            if pickupDist < pDistance[passenger]:
                candidates.append((passenger, pDistance[passenger] - pickupDist)
            else:
                taken.append((passenger, pDistance[passenger] - pickupDist))
    return (candidates + taken)[0]

def planCoffee(brain):
    """ Plan when to get coffee """
    return rand.choice(brain.stores).busStop

    
def allPickups(brain):
    me = brain.me
    passengers = brain.passengers
    """ Get an ordered list of passengers """
    pickup = [p for p in passengers if (not p in me.passengersDelivered and
                                        p != me.limo.passenger and
                                        p.car is None and
                                        p.lobby is not None and p.destination is not None)]
    rand.shuffle(pickup)
    return pickup


def rankPassengers(brain):
    """ Returns sorted list of (passenger, trip distance) """
    pass


def getBestStrategy(brain):
    """ returns Sort passengers by trip distance """
    # Rank passengers
    # Get best strategy for each enemy (and that passenger)
    # Consider enemy distance to passengers when deciding which to pick ups
    if brain.me.limo.passenger is not None:
        return handleCurrentPassenger(brain)
    elif brain.me.limo.coffeeServings <= 0:
        # Go get coffee
        return planCoffee(brain)
        
    pickup = allPickups(brain)
    brain.pickup = pickup
    return pickup[0].lobby.busStop


def handleCurrentPassenger(brain):
    """ Bring current passenger to their destination (or decide to abandon)"""
    assert(brain.me.limo.passenger is not None)
    return brain.me.limo.passenger.destination.busStop

def handleRefusedEnemy(brain):
    """ Handle case when passenger refuses to disembark """
    return rand.choice(filter(lambda c: c != brain.me.limo.passenger.destination,
        brain.companies)).busStop
    # Want to modify to drop off at closest location (or block opponent)
