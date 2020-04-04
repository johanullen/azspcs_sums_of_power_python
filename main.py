from time import time
import random
import math
from pprint import pprint
import traceback

import utils
from a import A


def brute_force(s, e, rand="all"):
    start = time()
    print(f"starting exp={e} with s={s}")
    a = A(s, e, rand)
    smallest = diff = a.diff()
    print(a.val, smallest, a)
    for i in a.riter_values():
        diff = a.diff()
        if abs(diff) < abs(smallest) or diff == 0:
            print(i, diff, a)
            smallest = diff
            if diff == 0:
                break
    timing = time() - start
    print(f"found smallest={smallest} after {i:e} iterations and {timing:.3f}s")
    print("*" * 40)


def greedy(s, e, initial="all"):
    start = time()
    print(f"starting exp={e} with s={s}", flush=True)
    a = A(s, e, initial)
    smallest = a.diff()

    history = {a.val}
    i = 0
    flip_or_rand = 0
    while smallest != 0:
        try:
            pos = a.get_most_impactful_bit()
            pos_sign = -1 if a.is_set(pos) else 1
            # need to check for loops
            tried = set()
            if (a.val + pos_sign * pos ** a.e) in history:
                flip_or_rand += 1
                if flip_or_rand % 1:
                    a.flip_all()
                else:
                    a.set_random()
                    history = {a.val}
                pos = a.get_most_impactful_bit()
                pos_sign = -1 if a.is_set(pos) else 1

            # if i % 2 == 0:
            history.add(a.val + pos_sign * pos ** a.e)
            a.flip_bit(pos)
        except:
            print("\titeration:", i)
            print("\tdiff:", a.diff())
            print("\tpos:", pos)
            print("\ta.val:", a.val)
            print("\tnew a.val:", (a.val + pos_sign * pos ** a.e))
            print("\ta.maxval:", a.maxval)
            print("\ta.vec:", a.vec.reverse())
            print("\ta:", a)
            print(f"\t{i}", f"|| {s**e}-{a.val}={a.diff()} => pos={pos} ||", a)
            raise

        diff = a.diff()
        if abs(diff) < abs(smallest) or diff == 0:
            # print(i, f"{(time() - start):.4f}s", f"|| {s**e}-{a.val}={diff} => pos={pos} ||", a, flush=True)
            smallest = diff
            if diff == 0:
                break
        i += 1

    timing = time() - start
    print(f"found smallest={smallest} after {i:10.2e} iterations and {timing:.3f}s", flush=True)
    return i, timing, a

if __name__ == "__main__":
    # [3,5,6,15,12,25,40,84,47,63,68,81,102,95,104],
    # for e, s in enumerate([3,5,6,15,12], 1):  # s>=6 are too big
    #     brute_force(s, e)
    res = list()
    for e, s in enumerate([3,5,6,15,12,25,40,84,47,63,68,81,102,95,104], 1):
        # s > 70? is too big
        if s > 41:
            continue
        try:
            res.append(greedy(s, e, "all"))
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
