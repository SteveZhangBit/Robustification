
import sys
from os import path

sys.path.append(path.dirname(path.dirname(path.dirname(path.abspath(__file__)))))

from repair import *

alphabet = ["back", "confirm", "password", "select", "vote",
            "v[1].enter","v[2].enter","v[1].exit","v[2].exit","eo[1].enter","eo[1].exit"
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
    progress=["confirm"],
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
        PRIORITY0: ["back", "confirm", "password", "select", "vote"]
    }
)

result = r.synthesize()
next(iter(result))
