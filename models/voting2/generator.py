import sys

def gen_env(n, m):
  return f'''
range N_VOTER = 1..{n}
range N_EO = 1..{m}

ENV = (v[i:N_VOTER].enter -> VOTER[i] | eo[j:N_EO].enter -> EO[j]),
VOTER[i:N_VOTER] = (password -> VOTER[i] | select -> VOTER[i] | vote -> VOTER[i] | confirm -> v[i].exit -> ENV | back -> VOTER[i] | v[i].exit -> ENV),
EO[j:N_EO] = (select -> EO[j] | vote -> EO[j] | confirm -> eo[j].exit -> ENV | back -> EO[j] | eo[j].exit -> ENV).
'''


def gen_p(n, m):
  return f'''
const NoBody = 0
const VOTERS = {n}

range N_VOTER = 1..{n}
range N_EO = 1..{m}

range WHO = NoBody..{m+n}

P = VOTE[NoBody][NoBody][NoBody],
VOTE[in:WHO][sel:WHO][v:WHO] = (
      v[i:N_VOTER].enter -> VOTE[i][sel][v] | eo[j:N_EO].enter -> VOTE[VOTERS+j][sel][v]
    | password -> VOTE[in][sel][in]
    | select -> VOTE[in][in][v]
    | when (sel == v) confirm -> VOTE[in][NoBody][NoBody]
).
'''


def gen_run(n, m):
  enter_exits = ",".join(
    [f'"v[{i}].enter"' for i in range(1, n+1)] +
    [f'"v[{i}].exit"' for i in range(1, n+1)] +
    [f'"eo[{j}].enter"' for j in range(1, m+1)] +
    [f'"eo[{j}].exit"' for j in range(1, m+1)]
  )
  return f'''
import sys
from os import path

sys.path.append(path.dirname(path.dirname(path.dirname(path.abspath(__file__)))))

from repair import *

alphabet = ["back", "confirm", "password", "select", "vote",
            {enter_exits}
            ]


r = Repair(
    alg="pareto",
    sys=["sys.lts"],
    env=["env.lts"],
    safety=["p.lts"],
    preferred={{   # rank the preferred behavior by importance
        PRIORITY3: ["back.lts"],
        PRIORITY2: [],
        PRIORITY1: [],
        PRIORITY0: []
    }},
    progress=["confirm"],
    alphabet=alphabet,  # \\alpha M \\union \\alpha E
    controllable={{  # rank the controllable events by cost
        PRIORITY3: [
          {enter_exits}
        ],
        PRIORITY2: [],
        PRIORITY1: [],
        PRIORITY0: ["back", "confirm", "password", "select", "vote"]
    }},
    observable={{    # rank observable events by cost
        PRIORITY3: [],
        PRIORITY2: [
          {enter_exits}
        ],
        PRIORITY1: [],
        PRIORITY0: ["back", "confirm", "password", "select", "vote"]
    }}
)

result = r.synthesize()
next(iter(result))
'''


if __name__ == "__main__":
  if len(sys.argv) < 3:
    print("Usage: generator.py <num of voters> <num of officials>")
    exit(0)
  n, m = int(sys.argv[1]), int(sys.argv[2])
  
  with open("env.lts", "w") as f:
    f.write(gen_env(n, m))
  
  with open("p.lts", "w") as f:
    f.write(gen_p(n, m))
  
  with open("run.py", "w") as f:
    f.write(gen_run(n, m))
