import random as rand
import simpleAStar

def tripDistance(brain, start, dest):
    """ Return shortest path distance between start and dest """
    print(start)
    print(dest)
    return len(simpleAStar.calculatePath(brain.gameMap, start, dest))


def totalTripDistance(brain, limo, passenger, needsCoffee=False):
    """ Calculate total distance from car->pickup->destination """

    # if the passenger is already in a limo or done w/ route, fuggedaboutit
    if passenger.car is not None or passenger.lobby is None:
        return (None, None)
 
    bestCoffeeShop = None

    if needsCoffee:
        firstLeg = float('inf')
        for coffeeShop in brain.stores: # fix this
            distance = tripDistance(brain, limo.tilePosition, coffeeShop.busStop) +  \
                        tripDistance(brain, coffeeShop.busStop, passenger.lobby)
            if distance < firstLeg:
                firstLeg = distance
                bestCoffeeShop = coffeeShop
    else:
        firstLeg = tripDistance(brain, limo.tilePosition, passenger.lobby.busStop)

    secondLeg = tripDistance(brain, passenger.lobby.busStop, passenger.destination.busStop)

    totalDistance = firstLeg + secondLeg

    return (totalDistance, bestCoffeeShop) # Placeholder

def getBestEnemyTarget(brain, enemy):
    enemyTripDistances = [totalTripDistance(brain, enemy.limo, passenger) for passenger in brain.passengers]
    bestTarget = min(enemyTripDistances)[0] # get total distance, ignore coffeeshop (should be None)
    pickupDistance = totalTripDistance(brain, enemy.limo, passenger)[0]
    return (bestTarget, pickupDistance)

def rankPassengers(brain, needsCoffee=False):
    openPassengers = [passenger for passenger in brain.passengers if passenger.car is None and passenger.lobby is not None]
    tripDistances = [totalTripDistance(brain, brain.me.limo, passenger, needsCoffee) for passenger in openPassengers]
    pointsDelivered = [passenger.pointsDelivered for passenger in openPassengers]
    ordered = sorted(zip(pointsDelivered, tripDistances, openPassengers), key=lambda x: (-x[0], x[1]))
    unzipped = zip(*ordered)
    return zip(unzipped[2], zip(*unzipped[1])[1]) # Get passengers, bestCoffeeShops tuple

def getOurBestPassenger(brain, needsCoffee=False):
    orderedPassengers = rankPassengers(brain, needsCoffee)
    p = orderedPassengers[0]
    return (p[0], 10, p[1])
    # enemyPassengers = [getBestEnemyTarget(brain, enemy) for enemy in brain.players if enemy != brain.me]
    # pDistance = dict(enemyPassengers)
    # candidates = []
    # taken = []
    # print(orderedPassengers)
    # for passenger, coffeeshop in orderedPassengers:
    #     if passenger in pDistance:
    #         pickupDist = tripDistance(brain, brain.me.limo.tilePosition, passenger.lobby)
    #         if pickupDist < pDistance[passenger]:
    #             candidates.append((passenger, pDistance[passenger] - pickupDist, coffeeshop))
    #         else:
    #             taken.append((passenger, pDistance[passenger] - pickupDist, coffeeshop))
    # return (candidates + taken)[0]

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


def getBestStrategy(brain):
    """ returns Sort passengers by trip distance """
    print("TICK")
    # Rank passengers
    # Get best strategy for each enemy (and that passenger)
    # Consider enemy distance to passengers when deciding which to pick ups
    if brain.me.limo.passenger is not None:
        return handleCurrentPassenger(brain)
    elif brain.me.limo.coffeeServings <= 0:
        # Go get coffee
        passenger, advantage, coffeeshop = getOurBestPassenger(brain, needsCoffee=True)
        return coffeeshop.busStop
    else:
        passenger, advantage, _ = getOurBestPassenger(brain, needsCoffee=False)
        print(passenger)
        brain.pickup = [passenger]
        return passenger.lobby.busStop

def handleCurrentPassenger(brain):
    """ Bring current passenger to their destination (or decide to abandon)"""
    assert(brain.me.limo.passenger is not None)
    return brain.me.limo.passenger.destination.busStop

def handleRefusedEnemy(brain):
    """ Handle case when passenger refuses to disembark """
    return rand.choice(filter(lambda c: c != brain.me.limo.passenger.destination,
        brain.companies)).busStop
    # Want to modify to drop off at closest location (or block opponent)
