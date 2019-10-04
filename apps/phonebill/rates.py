"""
    Tariff rules and static values for the calculation
    of each record of the telephone bill
"""


class PriceRates:

    FLAT_RATE = 0.36
    MINUTE = 0.09

    LIST_RATE = {
        MINUTE: "Minute",
        FLAT_RATE: "FlatRate"
    }

    RATES = tuple(LIST_RATE.items())
