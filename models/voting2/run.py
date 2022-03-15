
import sys
from os import path

sys.path.append(path.dirname(path.dirname(path.dirname(path.abspath(__file__)))))

from repair import *

alphabet = ["back", "confirm", "password", "select", "vote",
            "v[1].enter","v[2].enter","v[1].exit","v[2].exit","eo[1].enter","eo[1].exit",
            "v[1].done","v[2].done"
            ]


r = Repair(
    alg="pareto",
    sys=["sys.lts"],
    env=["env.lts"],
    safety=["p.lts"],
    preferred={   # rank the preferred behavior by importance
        PRIORITY3: ["back.lts"],
        PRIORITY2: [],
        PRIORITY1: [],
        PRIORITY0: []
    },
    progress=["v[1].done","v[2].done"],
    alphabet=alphabet,  # \alpha M \union \alpha E
    controllable={  # rank the controllable events by cost
        PRIORITY3: [
          "v[1].enter","v[2].enter","v[1].exit","v[2].exit","eo[1].enter","eo[1].exit"
        ],
        PRIORITY2: [],
        PRIORITY1: [],
        PRIORITY0: ["back", "confirm", "password", "select", "vote"]
    },
    observable={    # rank observable events by cost
        PRIORITY3: [],
        PRIORITY2: [
          "v[1].enter","v[2].enter","v[1].exit","v[2].exit","eo[1].enter","eo[1].exit"
        ],
        PRIORITY1: [],
        PRIORITY0: ["back", "confirm", "password", "select", "vote", "v[1].done","v[2].done"]
    }
)

result = r.synthesize()
cs = next(iter(result))
# count = 1
# for c in cs:
#     print("Solution", count)
#     print(r.fsm2fsp(c["M_prime"], c["observable"], name="M"))
#     count += 1
