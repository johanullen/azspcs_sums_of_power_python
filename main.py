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


def greedy(s, e, rand="all"):
    start = time()
    print(f"starting exp={e} with s={s}")
    a = A(s, e, rand)
    smallest = diff = a.diff()
    sign = utils.intsign(diff)
    pos = int(math.log(sign * diff, a.e)) if diff else None

    history = {a.val}
    print(history)
    i = 0
    while smallest != 0:
        try:
            # print(i, f"|| {s**e}-{a.val}={diff} => pos={pos} ||", a)
            sign = utils.intsign(diff)
            pos = int(math.log(sign * diff, a.e))

            # need to check wether pos it set
            pos_sign = -1 if a.is_set(pos) else 1

            # need to check for loops
            while (a.val + pos_sign * pos ** a.e) in history:
                # if pos < a.s-2:  # -2 because 0 indexation and stop one before
                if pos > 0:
                    pos += 1
                else:
                    pos = a.s-2 #0
                pos_sign = -1 if a.is_set(pos) else 1
            history.add(a.val + pos_sign * pos ** a.e)

            a.flip_bit(pos)
        except:
            print("\titeration:", i)
            print("\tdiff:", diff)
            print("\tpos:", pos)
            print("\ta.val:", a.val)
            print("\tnew a.val:", (a.val + pos_sign * pos ** a.e))
            print("\ta.maxval:", a.maxval)
            print("\ta.vec:", a.vec.reverse())
            print("\ta:", a)
            print(f"\t{i}", f"|| {s**e}-{a.val}={diff} => pos={pos} ||", a)
            print("history:", end=" ")
            pprint(history)
            raise

        prev = diff
        diff = a.diff()
        if abs(diff) < abs(smallest) or diff == 0:
            print(f"found new smallest {diff}")
            print(i, f"|| {s**e}-{a.val}={diff} => pos={pos} ||", a)
            smallest = diff
            if diff == 0:
                break
        i += 1

    timing = time() - start
    print(f"found smallest={smallest} after {i:e} iterations and {timing:.3f}s")
    print("*" * 40)

if __name__ == "__main__":
    # [3,5,6,15,12,25,40]
    for e, s in enumerate([3,5,6,15,12], 1):  # s>=6 are too big
        brute_force(s, e)

    for e, s in enumerate([3,5,6,15], 1):
        greedy(s, e, "all")

