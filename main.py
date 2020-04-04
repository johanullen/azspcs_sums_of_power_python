from time import time
import traceback

from algs.brute_force import brute_force
from algs.greedy_allow_overflow import greedy_allow_overflow

if __name__ == "__main__":
    # [3,5,6,15,12,25,40,84,47,63,68,81,102,95,104],
    res = list()
    for e, s in enumerate([3,5,6,15,12], 1):  # s>=6 are too big
        res.append(brute_force(s, e))
    for r in res:
        print(f"(n={r[2].e},s={r[2].s}) i={r[0]:10.2e},t={r[1]:.2f}s || {r[2]} ")

    res = list()
    for e, s in enumerate([3,5,6,15,12,25,40,84,47,63,68,81,102,95,104], 1):
        # s > 70? is too big
        if s > 41:
            continue
        try:
            res.append(greedy_allow_overflow(s, e, "all"))
        except:
            traceback.print_exc()
            break
    for r in res:
        print(f"(n={r[2].e},s={r[2].s}) i={r[0]:10.2e},t={r[1]:.2f}s || {r[2]} ")

# history: (n=1,s=3) i=  0.00e+00,t=0.00s || 3^1=>{1,2}
# (n=2,s=5) i=  1.00e+00,t=0.00s || 5^2=>{3,4}
# (n=3,s=6) i=  0.00e+00,t=0.00s || 6^3=>{3,4,5}
# (n=4,s=15) i=  4.90e+01,t=0.01s || 15^4=>{4,6,8,9,14}
# (n=5,s=12) i=  8.50e+01,t=0.01s || 12^5=>{4,5,6,7,9,11}
# (n=6,s=25) i=  1.30e+04,t=0.24s || 25^6=>{1,2,3,5,6,7,8,9,10,12,13,15,16,17,18,23}
# (n=7,s=40) i=  1.05e+05,t=0.58s || 40^7=>{1,3,5,9,12,14,16,17,18,20,21,22,25,28,39}
# (n=9,s=47) i=  2.22e+04,t=0.11s || 47^9=>{1,2,4,7,11,14,15,18,26,27,30,31,32,33,36,38,39,43}
# (n=10,s=63) i=  1.12e+08,t=515.23s || 63^10=>{1,2,4,5,6,8,12,15,16,17,20,21,25,26,27,28,30,36,37,38,40,51,62}
