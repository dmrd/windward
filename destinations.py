import random as rand

def distanceHeuristic(start, dest):
    """ Return squared Manhattan distance """
    x = dest[0] - start[0]
    y = dest[1] - start[1]
    return x*x + y*y


def totalTripDistance(car, passenger):
    """ Calculate total distance from car->pickup->destination """
    return 1  # Placeholder


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
