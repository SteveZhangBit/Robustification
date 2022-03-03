from itertools import count
import sys
from os import path

sys.path.append(path.dirname(path.dirname(path.dirname(path.abspath(__file__)))))

from repair import *

alphabet = ["m[1]","m[2]","m[3]","m[4]","m[5]","m[6]","m[7]","m[8]","m[1][2]","m[1][3]","m[1][4]","m[1][5]","m[1][6]","m[1][7]","m[1][8]","m[2][2]","m[2][3]","m[2][4]","m[2][5]","m[2][6]","m[2][7]","m[2][8]","m[3][2]","m[3][3]","m[3][4]","m[3][5]","m[3][6]","m[3][7]","m[3][8]","m[4][2]","m[4][3]","m[4][4]","m[4][5]","m[4][6]","m[4][7]","m[4][8]","m[5][2]","m[5][3]","m[5][4]","m[5][5]","m[5][6]","m[5][7]","m[5][8]","m[6][2]","m[6][3]","m[6][4]","m[6][5]","m[6][6]","m[6][7]","m[6][8]","m[7][2]","m[7][3]","m[7][4]","m[7][5]","m[7][6]","m[7][7]","m[7][8]","m[8][2]","m[8][3]","m[8][4]","m[8][5]","m[8][6]","m[8][7]","m[8][8]","s[1][5]","s[2][5]","s[3][5]","s[4][5]","s[5][5]","s[6][5]","s[7][5]","s[8][5]"]

r = Repair(
    alg="pareto",
    sys=["sys.lts"],
    env=["env.lts"],
    safety=["p.lts"],
    preferred={   # rank the preferred behavior by importance
        PRIORITY3: [],
        PRIORITY2: [],
        PRIORITY1: [],
        PRIORITY0: []
    },
    progress=["m[2]","m[3]","m[4]","m[5]","m[6]","m[7]","m[8]"],
    alphabet=alphabet,
    controllable={  # rank the controllable events by cost
        PRIORITY3: [],
        PRIORITY2: [],
        PRIORITY1: [],
        PRIORITY0: ["m[1]","m[2]","m[3]","m[4]","m[5]","m[6]","m[7]","m[8]"]
    },
    observable={    # rank observable events by cost
        PRIORITY3: [],
        PRIORITY2: ["m[4][5]","m[3][4]","m[4][3]","m[6][7]","m[8][2]","m[2][3]","m[6][5]","m[7][8]","m[3][2]","m[1][2]","m[5][6]","m[7][6]","m[5][4]","s[6][5]","s[4][5]","m[2][8]","m[8][7]"],
        PRIORITY1: ["m[2][2]","m[3][3]","m[4][4]","m[5][5]","m[6][6]","m[7][7]","m[8][8]","s[5][5]"],
        PRIORITY0: ["m[1]","m[2]","m[3]","m[4]","m[5]","m[6]","m[7]","m[8]"]
    }
)

result = r.synthesize()
cs = next(iter(result))