global targetMovePassenger
global targetChangeDestination
global targetStopCar
targetMovePassenger = targetChangeDestination = targetStopCar = None

import random
from simpleAStar import calculatePath

PLAY_THRESHOLD = 1
DISCARD_THRESHOLD = -1


# Returns positive (base 1) index of powerUp to be played or negative index of powerUp to be discarded; 0 otherwise
def choosepowerUp(brain):
    scoreIndex = []
    i = 1
    for powerUp in brain.powerUpHand:
        scoreIndex.append((_calculateScore(brain, powerUp), i))
        i += 1
    scoreIndex.sort()

    if scoreIndex[-1][0] > PLAY_THRESHOLD:
        return scoreIndex[-1][1]

    if scoreIndex[0][0] < DISCARD_THRESHOLD:
        return -scoreIndex[0][1]

    return 0


def _calculateScore(brain, powerUp):
    try:
        if powerUp.card == "MOVE_PASSENGER":
            return _calculateMovePassengerScore(brain)
        if powerUp.card == "CHANGE_DESTINATION":
            return _calculateChangeDestinationScore(brain)
        if powerUp.card == "MULT_DELIVERY_QUARTER_SPEED":
            return _calculateMultDeliveryQuarterSpeedScore(brain)
        if powerUp.card == "ALL_OTHER_CARS_QUARTER_SPEED":
            return _calculateAllOtherCarsQuarterSpeedScore(brain)
        if powerUp.card == "STOP_CAR":
            return _calculateStopCarScore(brain)
        if powerUp.card == "RELOCATE_ALL_CARS":
            return _calculateRelocateAllCarsScore(brain)
        if powerUp.card == "RELOCATE_ALL_PASSENGERS":
            return _calculateRelocateAllPassengersScore(brain)
        if powerUp.card == "MULT_DELIVERING_PASSENGER":
            return _calculateMultDeliveringPassengerScore(brain, powerUp.passenger)
        if powerUp.card == "MULT_DELIVER_AT_COMPANY":
            return _calculateMultDeliverAtCompanyScore(brain, powerUp.company)

    except:
        return random.choice([-2, 0, 0, 2, 2, 2])


def _calculateMovePassengerScore(brain):
    global targetMovePassenger

    K = 1 # TODO: mess with this

    passengerScores = []
    for company in brain.companies:
        if company.passengers is None or len(company.passengers) == 0:
            continue

        oppDistScore = 0
        for player in brain.players:
            if player == brain.me:
                continue
            oppDistScore += len(calculatePath(brain.gameMap, player.limo.tilePosition, player.limo.passenger.destination.busStop))
        oppDistScore /= 9

        myDistScore = len(calculatePath(brain.gameMap, brain.me.limo.tilePosition, brain.me.limo.passenger.destination.busStop))

        distScore = K/oppDistScore - K/myDistScore

        for passenger in company.passenger:
            passengerScores.add((passenger.pointsDelivered * distScore, passenger.name))

    passengerScores.sort()
    targetMovePassenger = passengerScores[-1][1]
    return passengerScores[-1][0]


def _calculateChangeDestinationScore(brain):
    global targetChangeDestination

    K = 1 # TODO: mess with this

    TOO_CLOSE = 9

    passengerScores = []

    for player in brain.players:
        if player == brain.me or player.limo.passenger is None:
            continue

        dist = len(calculatePath(brain.gameMap, player.limo.tilePosition, player.limo.passenger.destination.busStop))

        if dist < TOO_CLOSE:
            passengerScores.append((0, player.limo.passenger.name))
            continue

        passengerScores.append((K * player.limo.passenger.pointsDelivered / dist, player.limo.passenger.name))

    passengerScores.sort()
    targetChangeDestination = passengerScores[-1][1]
    return passengerScores[-1][0]


def _calculateMultDeliveryQuarterSpeedScore(brain):
    K = 0.1 # TODO: mess with this

    dist = len(calculatePath(brain.gameMap, brain.me.pickup[0].lobby.busStop, brain.me.pickup[0].destination.busStop))
    score = brain.me.pickup[0].pointsDelivered

    return K * score / dist


def _calculateAllOtherCarsQuarterSpeedScore(brain):
    K = 1 # TODO: mess with this

    passengerScores = []
    for company in brain.companies:
        if company.passengers is None or len(company.passengers) == 0:
            continue

        oppDistScore = 0
        for player in brain.players:
            if player == brain.me:
                continue
            oppDistScore += len(calculatePath(brain.gameMap, player.limo.tilePosition, player.limo.passenger.destination.busStop))
        oppDistScore /= 9

        for passenger in company.passenger:
            passengerScores.add((K * passenger.pointsDelivered / oppDistScore, passenger.name))

    if len(passengerScores) == 0:
        return 0
    return sum(passengerScores) / len(passengerScores)


def _calculateStopCarScore(brain):
    global targetStopCar

    K = 1 # TODO: mess with this

    playerScores = []
    for player in brain.players:
        distScore = len(calculatePath(brain.gameMap, player.limo.tilePosition, brain.me.pickup[0].lobby.busStop))
        playerScores.append((K * player.score * player.pickup[0].pointsDelivered / distScore, player.name))

    playerScores.sort()
    targetStopCar = playerScores[-1][1]
    return playerScores[-1][1]


def _calculateRelocateAllCarsScore(brain):
	K = 1 # TODO: HALP

	if brain.me.limo.passenger is None:
		myDist = len(calculatePath(brain.gameMap, brain.me.limo.tilePosition, brain.me.pickup[0].lobby.busStop))
		oppDist = 0
		for p in brain.players:
			oppDist += len(calculatePath(brain.gameMap, p.limo.tilePosition , brain.me.pickul[0].lobby.busStop))
		oppDist /= 9

		return K/oppDist - K/myDist

	else:
		return 0


def _calculateRelocateAllPassengersScore(brain):
    K = 1 # TODO: mess with this

    passengerScores = []
    for company in brain.companies:
        if company.passengers is None or len(company.passengers) == 0:
            continue

        oppDistScore = 0
        for player in brain.players:
            if player == brain.me:
                continue
            oppDistScore += len(calculatePath(brain.gameMap, player.limo.tilePosition, player.limo.passenger.destination.busStop))
        oppDistScore /= 9

        myDistScore = len(calculatePath(brain.gameMap, brain.me.limo.tilePosition, brain.me.limo.passenger.destination.busStop))

        distScore = K/oppDistScore - K/myDistScore

        for passenger in company.passenger:
            passengerScores.add((passenger.pointsDelivered * distScore, passenger.name))

    if len(passengerScores) == 0:
        return 0
    return sum(passengerScores) / len(passengerScores)


def _calculateMultDeliveringPassengerScore(brain, passenger):
    K = 1 # TODO: mess with this

    if passenger in brain.carried[brain.me.guid] or passenger not in brain.me.pickup:
        return -float("inf")

    if brain.me.limo.coffeeServings < 2:
        return -K * (brain.me.pickup.index(passenger) + 1)

    return K / (brain.me.pickup.index(passenger) + 1)


def _calculateMultDeliverAtCompanyScore(brain, company):
    K = 1 # TODO: mess with this

    destinations = (passenger.destination for passenger in brain.pickup)

    if len(destinations) == 0:
        return -float("inf")

    if brain.me.limo.coffeeServings < 2:
        return -K * (destinations.index(company) + 1)

    return K / (destinations.index(company) + 1)
