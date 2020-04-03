from BitVector import BitVector
import random
import utils


class A():

    def __init__(self, s=0, e=0, initial="all"):
        self.e = e
        self.s = s

        if initial.lower() == "all":
            self.vec = BitVector(size=self.s - 1)
            self.set_one()
        elif initial.lower() == "none":
            self.vec = BitVector(size=self.s - 1)
            self.set_zero()
        elif initial.lower() == "rand":
            self.vec = BitVector(size=self.s - 1)
            # for i in range(0, self.s - 1):
            #     self.vec[i] = random.randint(0, 1)
            self.set_random()
        else:
            raise ValueError(f'{initial}.lower() can be one of ["all", "none", "rand"]')
        self.maxval = sum(x**self.e for x in range(1, self.s))
        self.val = self.sum()

    def set_zero(self):
        self.vec.reset(0)
        self.val = 0

    def set_one(self):
        self.vec.reset(1)
        self.val = self.sum()

    def set_random(self):
        for i in range(0, self.s - 1):
            self.vec[i] = random.randint(0, 1)
        self.val = self.sum()


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

    def flip_all(self):
        for pos in range(self.s-1):
            self.flip_bit(pos)

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

    def get_best_bit(self, diff):
        sign = utils.intsign(diff)

        # pos_set represents if a bit should be set or unset
        # 0 is we want to change a bit to 0
        # 1 is we want to change a bit to 1
        # changing a bit to 0 corresponds to decreasing the signed difference
        # changing a bit to 1 corresponds to increasing the signed difference
        pos_set = 1 if sign == 1 else 0

        # -1 because the value of bit x is (x+1)**e
        root = abs(diff) ** (1 / self.e) - 1
        closest_pos = int(root + sign * 0.5)

        if self.vec.count_bits() > self.s // 2 and pos_set:
            # if there are more set bits than unset bits, and we want to change a bit from 1 to 0
            # then we want to travsere to lower values
            # because we want to remain on this side of the diff
            change_direction = -1
        elif self.vec.count_bits() > self.s // 2 and pos_set:
            # if there are more set unset bits than set bits, and we want to change a bit from 0 to 1
            # then we want to travsere to lower values
            # because we want to remain on this side of the diff
            change_direction = -1
        else:
            # otherwise we want to traverse to higher bits
            # because we want to change the sign of diff
            change_direction = 1

        if closest_pos >= self.s - 1:
            pos = self.s - 2
        elif closest_pos < 0:
            pos = 0
        else:
            pos = closest_pos

        # print("diff", diff)
        # print("sign", sign)
        # print("pos_set", pos_set)
        # print("root", root)
        # print("closest_pos", closest_pos)
        # print("change_direction", change_direction)
        # print("pos", pos)
        # print("self.vec[pos]", self.vec[pos])
        while self.vec[pos] == pos_set:
            # print(f"changing pos from {pos} to {pos + change_direction}")
            pos += change_direction
            if pos >= self.s - 1:
                # print(f"changing pos from {pos} to {0}")
                pos = 0
            if pos < 0:
                # print(f"changing pos from {pos} to {self.s - 2}")
                pos = self.s - 2
        return pos

    def get_most_impactful_bit(self):
        diff = self.diff()
        return self.get_best_bit(diff)



if __name__ == "__main__":
    for _ in range(20):
        a = A(4, 2, "rand")
        print(a)
