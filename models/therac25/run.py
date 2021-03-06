import sys
from os import path

sys.path.append(path.dirname(path.dirname(path.dirname(path.abspath(__file__)))))

from repair import *

alphabet = ["x", "e", "enter", "up", "b", "setMode", "fire_xray", "fire_ebeam"]

r = Repair(
    alg="pareto",
    sys=["sys.lts"],
    env=["env.lts"],
    safety =["p.lts"],
    preferred={   # rank the preferred behavior by importance
        PRIORITY3: ["back1.lts", "back2.lts"],
        PRIORITY2: ["back3.lts"],
        PRIORITY1: [],
        PRIORITY0: []
    },
    progress=["fire_xray", "fire_ebeam"],
    alphabet=alphabet,
    controllable={  # rank the controllable events by cost
        PRIORITY3: ["x", "e", "enter", "up", "b"],
        PRIORITY2: ["setMode"],
        PRIORITY1: ["fire_xray", "fire_ebeam"],
        PRIORITY0: []
    },
    observable={    # rank observable events by cost
        PRIORITY3: [],
        PRIORITY2: [],
        PRIORITY1: ["setMode"],
        PRIORITY0: ["x", "e", "enter", "up", "b", "fire_xray", "fire_ebeam"]
    }
)

result = r.synthesize()
next(iter(result))

# count = 1
# for cs in result:
#     for c in cs:
#         print("Solution", count)
#         print(r.fsm2fsp(c["M_prime"], c["observable"], name="M"))
#         count += 1
