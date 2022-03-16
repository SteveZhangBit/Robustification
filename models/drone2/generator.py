import sys


def gen_sys(n):
  spec = f"""\
const N = {n}
const Unknown = 0
const Front = 1
const Back = 2
range State = Unknown..Back

EGO = D[1],
D[e:1..N] = (
  d[e][i:1..N] -> if (i == e%N+1) then A[e][Front]
                  else if (e == 1 && i == N) then A[e][Back]
                  else if (e > 1 && i == (e-2)%N+1) then A[e][Back]
                  else A[e][Unknown]
),
A[e:1..N][s:State] = (
  when (s != Back) m[e] -> D[e] // stay
| when (s != Front) m[e%N+1] -> D[e%N+1] // move clockwise
| when (s == Front && e == 1) m[N] -> D[N] // move counter-clockwise
| when (s == Front && e > 1) m[(e-2)%N+1] -> D[(e-2)%N+1] // move counter-clockwise
).
"""
  return spec


def gen_env(n):
  spec = f"""\
const N = {n}

SRV = A[2],
A[i:1..N] = (
  d[1..N][i] -> A[i] // report current location
| c -> A[i%N+1] // move clockwise
| when (i == 1) b -> A[N] // move counter-clockwise
| when (i > 1) b -> A[(i-2)%N+1] // move counter-clockwise
).

TURN = TURN[0],
TURN[i:0..1] = (
  when (i == 0) d[1..N][1..N] -> m[1..N] -> TURN[1]
| when (i == 1) c -> TURN[0]
| when (i == 1) b -> TURN[0]
).
"""
  return spec


def gen_p(n):
  spec = f"""\
const N = {n}

property P = P[1][2],
P[e:1..N][s:1..N] = (
  m[i:1..N] -> if i != s then P[i][s] else ERROR
| c -> if s%N+1 != e then P[e][s%N+1] else ERROR
| when (s == 1) b -> if e != N then P[e][N] else ERROR
| when (s > 1) b -> if (s-2)%N+1 != e then P[e][(s-2)%N+1] else ERROR
).
"""
  return spec


def gen_run(n):
  ego_moves = ",".join([f'"m[{i}]"' for i in range(1, n+1)])
  ego_detects = ",\n    ".join([
    ",".join([f'"d[{i}][{j}]"' for i in range(1, n+1)])
    for j in range(1, n+1)
  ])
  obs_p0 = ",\n            ".join(
    [",".join(['"d[1][1]"', '"d[1][2]"', f'"d[1][{n}]"'])] +
    [",".join([f'"d[{i}][{i}]"', f'"d[{i}][{(i-2)%n+1}]"', f'"d[{i}][{i%n+1}]"']) for i in range(2, n+1)]
  )
  obs_p1 = ",\n            ".join(
    [",".join(['"d[1][3]"', f'"d[1][{n-1}]"'])] +
    [",".join(['"d[2][4]"', f'"d[2][{n}]"'])] +
    [",".join([f'"d[{i}][{(i+1)%n+1}]"', f'"d[{i}][{(i-3)%n+1}]"']) for i in range(3, n+1)]
  )
  spec = f'''\
import sys
from os import path

sys.path.append(path.dirname(path.dirname(path.dirname(path.abspath(__file__)))))

from repair import *

alphabet = [
    "b", "c",
    {ego_moves},
    {ego_detects},
]

r = Repair(
    alg="pareto",
    sys=["sys.lts"],
    env=["env.lts"],
    safety=["p.lts"],
    no_deadlock=True,
    preferred={{   # rank the preferred behavior by importance
        PRIORITY3: [],
        PRIORITY2: [],
        PRIORITY1: [],
        PRIORITY0: []
    }},
    progress=[{ego_moves}],
    alphabet=alphabet,  # \\alpha M \\union \\alpha E
    controllable={{  # rank the controllable events by cost
        PRIORITY3: [],
        PRIORITY2: [],
        PRIORITY1: [],
        PRIORITY0: [{ego_moves}]
    }},
    observable={{    # rank observable events by cost
        PRIORITY3: [],
        PRIORITY2: [],
        PRIORITY1: [
            {obs_p1},
        ],
        PRIORITY0: [
            {ego_moves},
            {obs_p0},
        ]
    }}
)

result = r.synthesize()
cs = next(iter(result))
# count = 1
# for c in cs:
#     print("Solution", count)
#     print(r.fsm2fsp(c["M_prime"], c["observable"], name="M"))
#     count += 1
'''
  return spec

if __name__ == "__main__":
  if len(sys.argv) < 2:
    print("Usage: generator.py n")
    exit(0)
  n = int(sys.argv[1])
  with open("sys.lts", "w") as f:
    f.write(gen_sys(n))
  with open("env.lts", "w") as f:
    f.write(gen_env(n))
  with open("p.lts", "w") as f:
    f.write(gen_p(n))
  with open("run.py", "w") as f:
    f.write(gen_run(n))
