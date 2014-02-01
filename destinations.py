import random as rand
import simpleAStar

def tripDistance(brain, start, dest):
    """ Return shortest path distance between start and dest """
    return len(simpleAStar.calculatePath(brain.gameMap, start, dest))


def totalTripDistance(brain, player, passenger, needsCoffee=False):
    """ Calculate total distance from car->pickup->destination """

    limo = player.limo
    if passenger in brain.carried[player.guid]:
        return (float('inf'), None)

    # if the passenger is already in a limo or done w/ route, fuggedaboutit
    if passenger.destination is None or passenger.lobby is None:
        return (float('inf'), None)
 
    if passenger.car is None: # passenger is free
        intermediateDestination = passenger.lobby
        finalDestination = passenger.destination
    else:
        intermediateDestination = passenger.destination
        if len(passenger.route) == 0:
            return (float('inf'), None)
        finalDestination = passenger.route[0][0]


    bestCoffeeShop = None

    if needsCoffee:
        firstLeg = float('inf')
        for coffeeShop in brain.stores: # fix this
            distance = tripDistance(brain, limo.tilePosition, coffeeShop.busStop) +  \
                        tripDistance(brain, coffeeShop.busStop, intermediateDestination.busStop)
            if distance < firstLeg:
                firstLeg = distance
                bestCoffeeShop = coffeeShop
    else:
        firstLeg = tripDistance(brain, limo.tilePosition, intermediateDestination.busStop)

    if passenger.car is not None:
        firstLeg = max(firstLeg, tripDistance(brain, passenger.car.tilePosition, intermediateDestination.busStop))

    secondLeg = tripDistance(brain, intermediateDestination.busStop, finalDestination.busStop)

    totalDistance = firstLeg + secondLeg

    return (totalDistance, bestCoffeeShop) # Placeholder

def getBestEnemyTarget(brain, enemy):
    enemyTripDistances = [totalTripDistance(brain, enemy, passenger) for passenger in brain.passengers]
    bestTarget = min(enemyTripDistances)[0] # get total distance, ignore coffeeshop (should be None)
    pickupDistance = totalTripDistance(brain, enemy, passenger)[0]
    return (bestTarget, pickupDistance)

def rankPassengers(brain, needsCoffee=False):
    openPassengers = [passenger for passenger in brain.passengers if passenger.car is None and passenger.lobby is not None]
    tripDistances = [totalTripDistance(brain, brain.me, passenger, needsCoffee) for passenger in openPassengers]
    pointsDelivered = [passenger.pointsDelivered for passenger in openPassengers]
    # ordered = sorted(zip(pointsDelivered, tripDistances, openPassengers), key=lambda x: x[1][0] / float(x[0]))
    ordered = sorted(zip(pointsDelivered, tripDistances, openPassengers), key=lambda x: x[1])
    unzipped = zip(*ordered)
    return zip(unzipped[2], zip(*unzipped[1])[1]) # Get passengers, bestCoffeeShops tuple

def getOurBestPassenger(brain, needsCoffee=False):
    orderedPassengers = rankPassengers(brain, needsCoffee)
    # return (orderedPassengers[0], 10, orderedPassengers[1]), zip(*orderedPassengers)[0]
    p = orderedPassengers[0]
    return (p[0], 10, p[1]), zip(*orderedPassengers)[0]


    ########################################################################################################
    # enemyPassengers = [getBestEnemyTarget(brain, enemy) for enemy in brain.players if enemy != brain.me] #
    # pDistance = dict(enemyPassengers)                                                                    #
    # candidates = []                                                                                      #
    # taken = []                                                                                           #
    # for passenger, coffeeshop in orderedPassengers:                                                      #
    #     if passenger in pDistance:                                                                       #
    #         pickupDist = tripDistance(brain, brain.me.limo.tilePosition, passenger.lobby)                #
    #         if pickupDist < pDistance[passenger]:                                                        #
    #             candidates.append((passenger, pDistance[passenger] - pickupDist, coffeeshop))            #
    #         else:                                                                                        #
    #             taken.append((passenger, pDistance[passenger] - pickupDist, coffeeshop))                 #
    #     else:                                                                                            #
    #         candidates.append((passenger, float('inf'), coffeeshop))                                     #
    # return (candidates + taken)[0], zip(*orderedPassengers)[0]                                           #
    ########################################################################################################

    
def getBestStrategy(brain):
    """ returns sorted passengers by trip distance """
    print("TICK")
    # Rank passengers
    # Get best strategy for each enemy (and that passenger)
    # Consider enemy distance to passengers when deciding which to pick ups
    print(brain.me.limo.passenger)
    if brain.me.limo.passenger is not None:
        print("HAVE A PASSENGER")
        return handleCurrentPassenger(brain)
    elif brain.me.limo.coffeeServings <= 0:
        # Go get coffee
        (passenger, advantage, coffeeshop), _ = getOurBestPassenger(brain, needsCoffee=True)
        return coffeeshop.busStop
    else:
        (passenger, advantage, _), preferences = getOurBestPassenger(brain, needsCoffee=False)
        print("Target: {}".format(passenger))
        brain.pickup = [passenger] + list(preferences)
        return passenger.lobby.busStop

def handleCurrentPassenger(brain):
    """ Bring current passenger to their destination (or decide to abandon)"""
    assert(brain.me.limo.passenger is not None)
    print("Current passenger: {}".format(brain.me.limo.passenger))
    return brain.me.limo.passenger.destination.busStop

def handleRefusedEnemy(brain):
    """ Handle case when passenger refuses to disembark """
    PRINT("ENEMY AT DESTINATION")
    companies = filter(lambda c: c != brain.me.limo.passenger.destination, brain.companies)
    distances = [tripDistance(brain, brain.me.limo.tilePosition, company.busStop)]
    return companies[ distances.index(min(distances)) ].busStop
    # Want to modify to drop off at closest location (or block opponent)
