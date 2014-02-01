global PLAY_THRESHOLD
global DISCARD_THRESHOLD
global multInPlay
global targetMovePassenger
global targetChangeDestination
global targetStopCar

PLAY_THRESHOLD = 1
DISCARD_THRESHOLD = -1

multInPlay = False


# Returns positive (base 1) index of powerup to be played or negative index of powerup to be discarded; 0 otherwise
def choosePowerup(powerups, status):
    scoreIndex = []
    i = 1
    for powerup in powerups:
        scoreIndex.append((_calculateScore(powerup, status), i))
        i += 1
    scoreIndex.sort()

    if scoreIndex[-1][0] >= PLAY_THRESHOLD:
        return powerups[scoreIndex[-1][1]]

    if scoreIndex[0][0] <= DISCARD_THRESHOLD:
        return -powerups[scoreIndex[0][1]]

    return 0


def _calculateScore(powerup, status):
    return 1 # naive for testing; remove

    if powerup.card == "MOVE_PASSENGER":
        return _calculateMovePassengerScore(status)
    if powerup.card == "CHANGE_DESTINATION":
        return _calculateChangeDestinationScore(status)
    if powerup.card == "MULT_DELIVERY_QUARTER_SPEED":
        return _calculateMultDeliveryQuarterSpeedScore(status)
    if powerup.card == "ALL_OTHER_CARS_QUARTER_SPEED":
        return _calculateAllOtherCarsQuarterSpeedScore(status)
    if powerup.card == "STOP_CAR":
        return _calculateStopCarScore(status)
    if powerup.card == "RELOCATE_ALL_CARS":
        return _calculateRelocateAllCars(status)
    if powerup.card == "RELOCATE_ALL_PASSENGERS":
        return _calculateRelocateAllPassengersScore(status)
    if powerup.card == "MULT_DELIVERING_PASSENGER":
        return _calculateMultDeliveringPassengerScore(status, powerup.passenger)
    if powerup.card == "MULT_DELIVER_AT_COMPANY":
        return _calculateMultDeliverAtCompany(status, powerup.company)


def _calculateMovePassengerScore(status):
    pass


def _calculateChangeDestinationScore(status):
    pass


def _calculateMultDeliveryQuarterSpeedScore(status):
    pass


def _calculateAllOtherCarsQuarterSpeedScore(status):
    pass


def _calculateStopCarScore(status):
    pass


def _calculateRelocateAllCars(status):
    pass


def _calculateRelocateAllPassengersScore(status):
    pass


def _calculateMultDeliveringPassengerScore(status, passenger):
    pass


def _calculateMultDeliverAtCompany(status, company):
    pass
