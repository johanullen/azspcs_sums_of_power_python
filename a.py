from BitVector import BitVector
import random
import utils


class A():

    def __init__(self, s=0, e=0, initial="all"):
        self.e = e
        self.s = s

        if initial.lower() == "all":
            self.vec = BitVector(size=self.s - 1)
            self.vec.reset(1)
        elif initial.lower() == "none":
            self.vec = BitVector(size=self.s - 1)
            self.vec.reset(0)
        elif initial.lower() == "rand":
            self.vec = BitVector(size=self.s - 1)
            for i in range(0, self.s - 1):
                self.vec[i] = random.randint(0, 1)
        else:
            raise ValueError(f'{initial}.lower() can be one of ["all", "none", "rand"]')
        self.maxval = sum(x**self.e for x in range(1, self.s))
        self.val = self.sum()

    def set_zero(self):
        self.vec.reset(0)
        self.val = 0

    def sum(self):
        sum_a = 0
        for ix, i in enumerate(self.vec, 1):
            sum_a += (ix * i) ** self.e
        return sum_a

    def diff(self):
        return self.s ** self.e - self.val

    def __str__(self):
        s = f"{self.s}^{self.e}=>" + "{"
        val_list = list()
        for ix, val in enumerate(self.vec, 1):
            if val:
                val_list.append(str(ix))
        s += ",".join(val_list)
        s += "}"
        return s

    def __repr__(self):
        return self.__str__()

    def __len__(self):
        return self.vec.__len__()

    def __iter__(self):
        return self.vec.__iter__()

    def flip_bit(self, pos):
        if pos < 0:
            raise OverflowError(f"trying to change bit {pos} < 0 ({(pos + 1) ** self.e} < {0})")
        elif pos >= self.s - 1:
            raise OverflowError(f"trying to change bit {pos} >= {self.s-1} ({(pos + 1) ** self.e} > {self.maxval})")
        self.val += -((pos + 1)**self.e) if self.vec[pos] else (pos + 1)**self.e
        self.vec[pos] = 0 if self.vec[pos] else 1
        return -((pos + 1)**self.e) if self.vec[pos] else (pos + 1)**self.e

    def add_one(self):
        for i in range(self.s):
            change = self.flip_bit(i)
            if self.vec[i]:
                break
        return change

    def sub_one(self):
        for i in range(self.s):
            change = self.flip_bit(i)
            if not self.vec[i]:
                break
        return change

    def iter_values(self):
        while True:
            yield self.val
            self.add_one()

    def riter_values(self):
        while True:
            yield self.val
            self.sub_one()

    def get_change(self, pos):
        change_sign = -1 if self.vec[pos] else 1
        change_value = (pos + 1) ** self.e
        return change_sign * change_value

    def is_set(self, pos):
        if pos < 0:
            raise OverflowError(f"trying to read bit {pos} < 0 ({(pos + 1) ** self.e} < {0})")
        elif pos >= self.s - 1:
            raise OverflowError(f"trying to read bit {pos} >= {self.s-1} ({(pos + 1) ** self.e} > {self.maxval})")
        return False if self.vec[pos] else True

    def get_pos_value(self, pos):
        return pos ** self.e

    def get_most_impactful_pos(self):
        diff = self.diff()
        sign = utils.intsign(diff)
        pos_set = 0 if sign == 1 else 1
        root = abs(diff) ** (1 / self.e)
        closest_pos = int(root + 0.5)
        if closest_pos >= self.s - 1:
            pos = self.s - 2
        elif closest_pos < 0:
            pos = 0
        else:
            pos = closest_pos
        while self.vec[pos] == pos_set:
            # todo change up if many are pos_set, otherwise change down
            pass


if __name__ == "__main__":
    for _ in range(20):
        a = A(4, 2, "rand")
        print(a)
