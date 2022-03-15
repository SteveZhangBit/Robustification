import sys
from os import path

sys.path.append(path.dirname(path.dirname(path.dirname(path.abspath(__file__)))))

from repair import *

alphabet = ["m[1]","m[2]","m[3]","m[4]","m[5]","m[1][2]","m[1][3]","m[1][4]","m[1][5]","m[2][2]","m[2][3]","m[2][4]","m[2][5]","m[3][2]","m[3][3]","m[3][4]","m[3][5]","m[4][2]","m[4][3]","m[4][4]","m[4][5]","m[5][2]","m[5][3]","m[5][4]","m[5][5]","s[1][5]","s[2][5]","s[3][5]","s[4][5]","s[5][5]"]

r = Repair(
    alg="pareto",
    no_deadlock=True,
    sys=["sys.lts"],
    env=["env.lts"],
    safety=["p.lts"],
    preferred={   # rank the preferred behavior by importance
        PRIORITY3: [],
        PRIORITY2: [],
        PRIORITY1: [],
        PRIORITY0: []
    },
    progress=[],
    alphabet=alphabet,
    controllable={  # rank the controllable events by cost
        PRIORITY3: [],
        PRIORITY2: [],
        PRIORITY1: [],
        PRIORITY0: ["m[1]","m[2]","m[3]","m[4]","m[5]"]
    },
    observable={    # rank observable events by cost
        PRIORITY3: [],
        PRIORITY2: ["m[5][4]","m[1][2]","m[3][4]","m[3][2]","m[4][5]","s[4][5]","s[2][5]","m[5][2]","m[2][3]","m[2][5]","m[4][3]"],
        PRIORITY1: ["m[2][2]","m[3][3]","m[4][4]","m[5][5]","s[5][5]"],
        PRIORITY0: ["m[1]","m[2]","m[3]","m[4]","m[5]"]
    }
)

result = r.synthesize()
cs = next(iter(result))
# count = 1
# for c in cs:
#     print("Solution", count)
#     print(r.fsm2fsp(c["M_prime"], c["observable"], name="M"))
#     count += 1
