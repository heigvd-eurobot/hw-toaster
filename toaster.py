from itertools import chain, permutations
from math import pow

E12 = [1.0, 1.2, 1.5, 1.8, 2.2, 2.4, 2.7, 3.3, 3.9, 5.6, 6.8, 8.2]
E24 = [1.0, 1.1, 1.2, 1.3, 1.5, 1.6, 1.8, 2.0, 2.2, 2.4, 2.7, 3.0,
       3.3, 3.6, 3.9, 4.3, 4.7, 5.1, 5.6, 6.2, 6.8, 7.5, 8.2, 9.1]

exp = [pow(10, i) for i in range(1, 5)]
resistors = list(chain.from_iterable([[round(x * e, 1) for e in E12] for x in [1e2, 1e3, 1e4, 1e5]]))

Vref = 10.8
Vthl, Vthh = 24, 26

def par(a, b): return a * b / (a + b)

def sys(r10, r12, r14, r8=10000):
    return (
        round(Vref / (par(r14, r12) / (par(r14, r12) + r10)), 2),
        round(Vref / (r14 / (r14 + par(r10, r12 + r8))), 2)
    )

all_solutions = [(sys(*u), u) for u in permutations(resistors, 4)]

s1 = [s for s in all_solutions if pow(Vthh - s[0][0], 2) + pow(Vthl - s[0][1], 2) < 0.1]
s2 = [s for s in s1 if s[1][0] + s[1][2] > 10000]
s3 = [s for s in s2 if s[1][3] >= 5000 and s[1][3] <= 30000]

sorted(
    [(round(pow(Vthh - x[0], 2) + pow(Vthl - x[1], 2), 3), u, x)
     for x, u in s3],
    key=lambda x: x[0],
)[:10]


# e1 = sp.Eq(par(r14, r12) / (par(r14, r12) + r10), Vref / Vthh)
# e2 = sp.Eq(r14 / (r14 + par(r10, r12 + r8)), Vref / Vthl)
