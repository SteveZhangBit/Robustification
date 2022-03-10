import sys


def gen_sys(n):
  spec = f"""\
const N = {n}

EGO = A[1][2],
A[e:1..N][s:2..N] = (
  when ((s-1)%(N-1)+2 != e) m[e] -> A[e][(s-1)%(N-1)+2] // stay
| when (e == 1 && s != 2 && (s-1)%(N-1)+2 != 2) m[2] -> A[2][(s-1)%(N-1)+2]
| when (e == 2) m[1] -> A[1][(s-1)%(N-1)+2]
| when (e > 1 && (e-1)%(N-1)+2 != s) m[(e-1)%(N-1)+2] -> A[(e-1)%(N-1)+2][(s-1)%(N-1)+2] // move clockwise
| when (e > 2 && (e-3)%(N-1)+2 != s && (e-3)%(N-1)+2 != (s-1)%(N-1)+2)
    m[(e-3)%(N-1)+2] -> A[(e-3)%(N-1)+2][(s-1)%(N-1)+2] // move counter-clockwise
| when (e == 2 && s != N && s != N-1) m[N] -> A[N][(s-1)%(N-1)+2]
).
"""
  return spec


def gen_env(n, stay):
  stay_const = "\n".join([f"const S{s} = {s}" for s in stay])
  stay_when = "\n| ".join([
    f"when (i == S{s}) s[1..N][S{s}] -> A[S{s}]" for s in stay
  ])
  stay_turn = "\n| ".join([
    f"when (i == 1) s[e][S{s}] -> TURN[0][e][S{s}]" for s in stay
  ])
  spec = f"""\
const N = {n}
{stay_const}

SRV = A[2],
A[i:2..N] = (
  m[1..N][i] -> A[(i-1)%(N-1)+2] // move clockwise
| {stay_when}
).

TURN = TURN[0][1][2],
TURN[i:0..1][e:1..N][s:2..N] = (
  when (i == 0) m[t:1..N] -> TURN[1][t][s]
| when (i == 1) m[e][s] -> TURN[0][e][(s-1)%(N-1)+2]
| {stay_turn}
).
"""
  return spec


def gen_p(n, stay):
  stay_const = "\n".join([f"const S{s} = {s}" for s in stay])
  stay_error = "\n| ".join([
    f"s[e][S{s}] -> if e != S{s} then P[e][S{s}] else ERROR" for s in stay
  ])
  spec = f"""\
const N = {n}
{stay_const}

property P = P[1][2],
P[e:1..N][s:2..N] = (
  m[t:1..N] -> if t != s then P[t][s] else ERROR
| m[e][s] -> if (s-1)%(N-1)+2 != e then P[e][(s-1)%(N-1)+2] else ERROR
| {stay_error}
).
"""
  return spec


def gen_run(n, stay):
  alphabet = [f'"m[{i}]"' for i in range(1, n+1)] + \
    [f'"m[{i}][{j}]"' for i in range(1, n+1) for j in range(2, n+1)]
  for s in stay:
    alphabet += [f'"s[{i}][{s}]"' for i in range(1, n+1)]
  alphabet = ",".join(alphabet)

  progress = ",".join([f'"m[{i}]"' for i in range(2, n+1)])
  controllable = ",".join([f'"m[{i}]"' for i in range(1, n+1)])

  obs_p0 = ",".join([f'"m[{i}]"' for i in range(1, n+1)])
  
  obs_p1 = ",".join([f'"m[{i}][{i}]"' for i in range(2, n+1)] +
    [f'"s[{s}][{s}]"' for s in stay])

  obs_p2 = ['"m[1][2]"', f'"m[2][{n}]"'] +\
    [f'"m[{i}][{(i-1)%(n-1)+2}]"' for i in range(2, n+1)] +\
    [f'"m[{i}][{(i-3)%(n-1)+2}]"' for i in range(3, n+1)]
  for s in stay:
    obs_p2 += [f'"s[{(s-1)%(n-1)+2}][{s}]"']
    if s == 2:
      obs_p2 += [f'"s[{n}][{s}]", f"s[1][{s}]"']
    else:
      obs_p2 += [f'"s[{(s-3)%(n-1)+2}][{s}]"']
  obs_p2 = ",".join(set(obs_p2))

  obs_p3 = ['"m[1][3]"', f'"m[1][{n}]"', f'"m[2][{n-1}]"', f'"m[3][{n}]"'] +\
    [f'"m[{i}][{i%(n-1)+2}]"' for i in range(2, n+1)] +\
    [f'"m[{i}][{(i-4)%(n-1)+2}]"' for i in range(4, n+1)]
  for s in stay:
    obs_p3 += [f'"s[{s%(n-1)+2}][{s}]"']
    if s == 2:
      obs_p3 += [f'"s[{n-1}][{s}]"']
    elif s == 3:
      obs_p3 += [f'"s[{n}][{s}]"', f'"s[1][{s}]"']
    else:
      obs_p3 += [f'"s[{(s-4)%(n-1)+2}][{s}]"']
    if s == n:
      obs_p3 += [f'"s[1][{s}]"']
  obs_p3 = ",".join(set(obs_p3))

  spec = f'''\
import sys
from os import path

sys.path.append(path.dirname(path.dirname(path.dirname(path.abspath(__file__)))))

from repair import *

alphabet = [{alphabet}]

r = Repair(
    alg="pareto",
    no_deadlock=True,
    sys=["sys.lts"],
    env=["env.lts"],
    safety=["p.lts"],
    preferred={{   # rank the preferred behavior by importance
        PRIORITY3: [],
        PRIORITY2: [],
        PRIORITY1: [],
        PRIORITY0: []
    }},
    progress=[],
    alphabet=alphabet,
    controllable={{  # rank the controllable events by cost
        PRIORITY3: [],
        PRIORITY2: [],
        PRIORITY1: [],
        PRIORITY0: [{controllable}]
    }},
    observable={{    # rank observable events by cost
        PRIORITY3: [],
        PRIORITY2: [{obs_p2}],
        PRIORITY1: [{obs_p1}],
        PRIORITY0: [{obs_p0}]
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
  if len(sys.argv) < 3:
    print("Usage: generator.py n stay...")
    exit(0)
  n = int(sys.argv[1])
  stay = list(map(lambda x: int(x), sys.argv[2:]))
  with open("sys.lts", "w") as f:
    f.write(gen_sys(n))
  with open("env.lts", "w") as f:
    f.write(gen_env(n, stay))
  with open("p.lts", "w") as f:
    f.write(gen_p(n, stay))
  with open("run.py", "w") as f:
    f.write(gen_run(n, stay))
