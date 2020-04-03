from time import time
import random
import math
from pprint import pprint

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
    print(f"starting exp={e} with s={s}")
    a = A(s, e, initial)
    smallest = a.diff()

    history = {a.val}
    i = 0
    while smallest != 0:
        # print("*"*40)
        try:
            pos = a.get_most_impactful_bit()
            pos_sign = -1 if a.is_set(pos) else 1
            # print(f"  {i}", f"|| {s**e}-{a.val}={a.diff()} => pos={pos} ||", a)
            # need to check for loops
            tried = set()
            if (a.val + pos_sign * pos ** a.e) in history:
                a.set_random()
                pos = a.get_most_impactful_bit()
                pos_sign = -1 if a.is_set(pos) else 1
            # while (a.val + pos_sign * pos ** a.e) in history:
            #     tried.add(pos)
            #     # if pos < a.s-2:  # -2 because 0 indexation and stop one before
            #     if pos < a.s - 2:
            #         pos += 1
            #     else:
            #         pos = a.s - 2  #0
            #     pos_sign = -1 if a.is_set(pos) else 1
            #     # reset to random when in loop
            #     if pos in tried:
            #         a.set_random()
            #         pos = a.get_most_impactful_bit()
            #         pos_sign = -1 if a.is_set(pos) else 1

            if i % 13 == 0:
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
            print("history:", end=" ")
            # pprint(history)
            raise

        diff = a.diff()
        if abs(diff) < abs(smallest) or diff == 0:
            # print(f"found new smallest {diff}")
            # print(i, f"{(time() - start):.4f}s", f"|| {s**e}-{a.val}={diff} => pos={pos} ||", a)
            smallest = diff
            if diff == 0:
                break
        i += 1

    timing = time() - start
    print(f"found smallest={smallest} after {i:10.2e} iterations and {timing:.3f}s")
    # print("*" * 40)
    return i, timing, a

if __name__ == "__main__":
    # [3,5,6,15,12,25,40,84,47,63,68,81],
    # for e, s in enumerate([3,5,6,15,12,25,40,84,47,63,68,81], 1):  # s>=6 are too big
    #     brute_force(s, e)
    res = list()
    for e, s in enumerate([3,5,6,15,12,25,40,84,47,63,68,81], 1):
        try:
            res.append(greedy(s, e, "all"))
        except:
            break
    for r in res:
        print(f"(n={r[2].e},s={r[2].s}) i={r[0]:10.2e},t={r[1]:.2f}s || {r[2]} ")

