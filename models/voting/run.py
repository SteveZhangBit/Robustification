import sys
from os import path

sys.path.append(path.dirname(path.dirname(path.dirname(path.abspath(__file__)))))

from repair import *

alphabet = ["back", "confirm", "password", "select", "vote",
            "eo.enter", "eo.exit", "v.enter", "v.exit"]


r = Repair(
    alg="pareto",
    sys=["sys.lts"],
    env=["env2.lts"],
    safety=["p.lts"],
    preferred={   # rank the preferred behavior by importance
        PRIORITY3: ["back.lts"],
        PRIORITY2: [],
        PRIORITY1: [],
        PRIORITY0: []
    },
    progress=["confirm"],
    alphabet=alphabet,  # \alpha M \union \alpha E
    controllable={  # rank the controllable events by cost
        PRIORITY3: ["eo.enter", "eo.exit", "v.enter", "v.exit"],
        PRIORITY2: [],
        PRIORITY1: [],
        PRIORITY0: ["back", "confirm", "password", "select", "vote"]
    },
    observable={    # rank observable events by cost
        PRIORITY3: [],
        PRIORITY2: ["eo.exit", "v.exit", "eo.enter", "v.enter"],
        PRIORITY1: [],
        PRIORITY0: ["back", "confirm", "password", "select", "vote"]
    }
)

result = r.synthesize()
count = 1
for cs in result:
    for c in cs:
        print("Solution", count)
        print(r.fsm2fsp(c["M_prime"], c["observable"], name="M"))
        count += 1
