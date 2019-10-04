"""
    Types of calls. Set to START calls and END calls
"""


class CallTypes:
    START = 1
    END = 2

    LIST_TYPE = {
        START: "Start",
        END: "End"
    }

    CHOICES = tuple(LIST_TYPE.items())
