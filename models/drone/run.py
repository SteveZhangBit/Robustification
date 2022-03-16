from itertools import count
import sys
from os import path

sys.path.append(path.dirname(path.dirname(path.dirname(path.abspath(__file__)))))

from repair import *

alphabet = [
    "b", "c",
    "m[1]", "m[2]", "m[3]", "m[4]", "m[5]",
    "d[1][1]", "d[2][1]", "d[3][1]", "d[4][1]", "d[5][1]",
    "d[1][2]", "d[2][2]", "d[3][2]", "d[4][2]", "d[5][2]",
    "d[1][3]", "d[2][3]", "d[3][3]", "d[4][3]", "d[5][3]",
    "d[1][4]", "d[2][4]", "d[3][4]", "d[4][4]", "d[5][4]",
    "d[1][5]", "d[2][5]", "d[3][5]", "d[4][5]", "d[5][5]",
]


r = Repair(
    alg="fast",
    sys=["sys.lts"],
    env=["env.lts"],
    safety=["p.lts"],
    no_deadlock=True,
    preferred={   # rank the preferred behavior by importance
        PRIORITY3: [],
        PRIORITY2: [],
        PRIORITY1: [],
        PRIORITY0: []
    },
    progress=["m[1]", "m[2]", "m[3]", "m[4]", "m[5]"],
    alphabet=alphabet,  # \alpha M \union \alpha E
    controllable={  # rank the controllable events by cost
        PRIORITY3: [],
        PRIORITY2: [],
        PRIORITY1: [],
        PRIORITY0: ["m[1]", "m[2]", "m[3]", "m[4]", "m[5]"]
    },
    observable={    # rank observable events by cost
        PRIORITY3: [],
        PRIORITY2: [],
        PRIORITY1: [
            "d[1][3]", "d[1][4]",
            "d[2][4]", "d[2][5]",
            "d[3][5]", "d[3][1]",
            "d[4][1]", "d[4][2]",
            "d[5][2]", "d[5][3]"
        ],
        PRIORITY0: [
            "m[1]", "m[2]", "m[3]", "m[4]", "m[5]",
            "d[1][1]", "d[1][2]", "d[1][5]",
            "d[2][2]", "d[2][1]", "d[2][3]",
            "d[3][3]", "d[3][2]", "d[3][4]",
            "d[4][4]", "d[4][3]", "d[4][5]",
            "d[5][5]", "d[5][4]", "d[5][1]"
        ]
    }
)

result = r.synthesize()
cs = next(iter(result))
# count = 1
# for c in cs:
#     print("Solution", count)
#     print(r.fsm2fsp(c["M_prime"], c["observable"], name="M"))
#     count += 1
