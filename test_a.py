from BitVector import BitVector
import unittest
from a import A


class TestA(unittest.TestCase):
    def test_init_all_ones(self):
        s = 5
        e = 2
        a = A(s, e, "all")
        self.assertEqual(a.e, e)
        self.assertEqual(a.s, s)
        self.assertEqual(a.maxval, 1 + 4 + 9 + 16)
        self.assertEqual(a.val, 1 + 4 + 9 + 16)
        self.assertEqual(a.vec, BitVector(intVal=2**(s - 1) - 1))
        self.assertEqual(a.bits_set, s - 1)

    def test_init_all_zeros(self):
        s = 5
        e = 2
        a = A(s, e, "none")
        self.assertEqual(a.e, e)
        self.assertEqual(a.s, s)
        self.assertEqual(a.maxval, 1 + 4 + 9 + 16)
        self.assertEqual(a.val, 0)
        self.assertEqual(a.vec, BitVector(bitlist=[0] * (s - 1)))
        self.assertEqual(a.bits_set, 0)

    def test_init_all_rand_s5_e2(self):
        s = 5
        e = 2
        a = A(s, e, "rand")
        self.assertEqual(a.e, e)
        self.assertEqual(a.s, s)
        self.assertEqual(a.maxval, 1 + 4 + 9 + 16)
        self.assertEqual(a.vec.length(), s - 1)
        self.assertLessEqual(a.val, 1 + 4 + 9 + 16)
        self.assertGreaterEqual(a.val, 0)
        self.assertEqual(a.bits_set, sum(a.vec))

    def test_init_all_rand_s3_e1(self):
        s = 3
        e = 1
        a = A(s, e, "rand")
        self.assertEqual(a.e, e)
        self.assertEqual(a.s, s)
        self.assertEqual(a.maxval, 1 + 2)
        self.assertEqual(a.vec.length(), s - 1)
        self.assertLessEqual(a.val, 1 + 2)
        self.assertGreaterEqual(a.val, 0)

    def test_init_raises_ValueError(self):  # noqa: N802
        s = 5
        e = 2
        with self.assertRaises(ValueError):
            A(s, e, "wrong!")

    def test_init_s5_e2(self):
        s = 5
        e = 2
        a = A(s, e)
        self.assertEqual(a.e, e)
        self.assertEqual(a.s, s)
        self.assertEqual(a.maxval, 1 + 4 + 9 + 16)
        self.assertEqual(a.val, 1 + 4 + 9 + 16)
        self.assertEqual(a.vec, BitVector(intVal=2**(s - 1) - 1))

    def test_init_s4_e4(self):
        s = 4
        e = 4
        a = A(s, e)
        self.assertEqual(a.e, e)
        self.assertEqual(a.s, s)
        self.assertEqual(a.maxval, 1 + 16 + 81)
        self.assertEqual(a.val, 1 + 16 + 81)
        self.assertEqual(a.vec, BitVector(intVal=2**(s - 1) - 1))

    def test_sum_s5_e2(self):
        s = 5
        e = 2
        a = A(s, e)
        self.assertEqual(a.sum(), 1 + 4 + 9 + 16)

    def test_sum_s4_e4(self):
        s = 4
        e = 4
        a = A(s, e)
        self.assertEqual(a.sum(), 1 + 16 + 81)

    def test_diff_s5_e2(self):
        s = 5
        e = 2
        a = A(s, e)
        self.assertEqual(a.diff(), 5**2 - (1 + 4 + 9 + 16))

    def test_diff_s4_e4(self):
        s = 4
        e = 4
        a = A(s, e)
        self.assertEqual(a.diff(), 4**4 - (1 + 16 + 81))

    def test_set_zero_s5_e2(self):
        s = 5
        e = 2
        a = A(s, e)
        self.assertEqual(a.val, 1 + 4 + 9 + 16)
        a.set_zero()
        self.assertEqual(a.val, 0)
        self.assertEqual(a.bits_set, 0)

    def test_set_zero_s4_e4(self):
        s = 4
        e = 4
        a = A(s, e)
        self.assertEqual(a.val, 1 + 16 + 81)
        a.set_zero()
        self.assertEqual(a.val, 0)
        self.assertEqual(a.bits_set, 0)

    def test_flip_bit_s5_e2(self):
        s = 5
        e = 2
        a = A(s, e)
        self.assertEqual(a.vec, BitVector(bitlist=[1, 1, 1, 1]))
        self.assertEqual(a.bits_set, 4)
        self.assertEqual(a.val, 1 + 4 + 9 + 16)
        a.flip_bit(0)
        self.assertEqual(a.vec, BitVector(bitlist=[0, 1, 1, 1]))
        self.assertEqual(a.val, 4 + 9 + 16)
        self.assertEqual(a.bits_set, 3)
        a.flip_bit(3)
        self.assertEqual(a.vec, BitVector(bitlist=[0, 1, 1, 0]))
        self.assertEqual(a.val, 4 + 9)
        self.assertEqual(a.bits_set, 2)
        with self.assertRaises(OverflowError):
            a.flip_bit(4)
        with self.assertRaises(OverflowError):
            a.flip_bit(-1)

    def test_addone_s5_e2(self):
        s = 5
        e = 2
        a = A(s, e)
        self.assertEqual(a.val, 1 + 4 + 9 + 16)
        with self.assertRaises(OverflowError):
            a.add_one()
        a.set_zero()
        self.assertEqual(a.val, 0)
        a.add_one()
        self.assertEqual(a.vec, BitVector(bitlist=[1, 0, 0, 0]))
        self.assertEqual(a.sum(), 1)
        self.assertEqual(a.val, 1)
        a.add_one()
        self.assertEqual(a.val, 4)
        a.add_one()
        self.assertEqual(a.val, 5)
        a.add_one()
        self.assertEqual(a.val, 9)

    def test_addone_s3_e1_add_one_to_one_less_than_max(self):
        s = 3
        e = 1
        a = A(s, e)
        self.assertEqual(a.val, 1 + 2)
        self.assertEqual(a.vec, BitVector(bitlist=[1, 1]))
        a.sub_one()
        self.assertEqual(a.val, 2)
        self.assertEqual(a.vec, BitVector(bitlist=[0, 1]))
        a.add_one()
        self.assertEqual(a.val, 1 + 2)
        self.assertEqual(a.vec, BitVector(bitlist=[1, 1]))

    def test_addone_s3_e1_sub_one_from_one(self):
        s = 3
        e = 1
        a = A(s, e)
        a.set_zero()
        self.assertEqual(a.val, 0)
        self.assertEqual(a.vec, BitVector(bitlist=[0, 0]))
        a.add_one()
        self.assertEqual(a.val, 1)
        self.assertEqual(a.vec, BitVector(bitlist=[1, 0]))
        a.sub_one()
        self.assertEqual(a.val, 0)
        self.assertEqual(a.vec, BitVector(bitlist=[0, 0]))

    def test_sub_s5_e2(self):
        s = 5
        e = 2
        a = A(s, e)
        self.assertEqual(a.val, 1 + 4 + 9 + 16)
        self.assertEqual(a.vec, BitVector(bitlist=[1, 1, 1, 1]))
        a.sub_one()
        self.assertEqual(a.vec, BitVector(bitlist=[0, 1, 1, 1]))
        self.assertEqual(a.sum(), 4 + 9 + 16)
        self.assertEqual(a.val, 4 + 9 + 16)
        a.sub_one()
        self.assertEqual(a.vec, BitVector(bitlist=[1, 0, 1, 1]))
        self.assertEqual(a.val, 1 + 9 + 16)
        a.sub_one()
        self.assertEqual(a.vec, BitVector(bitlist=[0, 0, 1, 1]))
        self.assertEqual(a.val, 9 + 16)
        a.sub_one()
        self.assertEqual(a.vec, BitVector(bitlist=[1, 1, 0, 1]))
        self.assertEqual(a.val, 1 + 4 + 16)
        a.set_zero()
        self.assertEqual(a.val, 0)
        with self.assertRaises(OverflowError):
            a.sub_one()

    def test_iter_value_s5_e2(self):
        s = 5
        e = 2
        a = A(s, e)
        itr = a.iter_values()
        self.assertEqual(next(itr), 30)
        with self.assertRaises(OverflowError):
            next(itr)
        a.set_zero()
        self.assertEqual(a.val, 0)

        for expected, actual in zip([0, 1, 4, 5, 9, 10, 13, 14, 16, 17, 20, 21, 25, 26, 29, 30], a.iter_values()):
            self.assertEqual(actual, expected)
            self.assertEqual(a.val, expected)

    def test_iter_value_s3_e1(self):
        s = 3
        e = 1
        a = A(s, e)
        a.set_zero()
        self.assertEqual(a.val, 0)
        for expected, actual in zip([0, 1, 2, 3], a.iter_values()):
            self.assertEqual(actual, expected)
            self.assertEqual(a.val, expected)

    def test_riter_value_s5_e2(self):
        s = 5
        e = 2
        a = A(s, e)
        self.assertEqual(a.val, 30)
        for expected, actual in zip([30, 29, 26, 25, 21, 20, 17, 16, 14, 13, 10, 9, 5, 4, 1, 0], a.riter_values()):
            self.assertEqual(actual, expected)
            self.assertEqual(a.val, expected)

    def test_riter_value_s5_e2_raises_OverflowError(self):
        s = 5
        e = 2
        a = A(s, e)
        a.set_zero()
        itr = a.riter_values()
        self.assertEqual(next(itr), 0)
        with self.assertRaises(OverflowError):
            next(itr)

    def test_riter_value_s3_e1(self):
        s = 3
        e = 1
        a = A(s, e)
        self.assertEqual(a.val, 3)

        for actual, expected in zip([3, 2, 1, 0], a.riter_values()):
            self.assertEqual(actual, expected)
            self.assertEqual(a.val, expected)

    def test_riter_value_s3_e1_raises_OverflowError(self):
        s = 3
        e = 1
        a = A(s, e)
        a.set_zero()
        itr = a.riter_values()
        self.assertEqual(next(itr), 0)
        with self.assertRaises(OverflowError):
            next(itr)

    def test_get_change(self):
        s = 3
        e = 1
        a = A(s, e)
        self.assertEqual(a.get_change(0), -1)
        self.assertEqual(a.get_change(1), -2)

    def test_get_best_bit__pebbif(self):
        """
        positive_exactly_best_bit_is_free
        """
        s = 5
        e = 2
        for test_bit in range(s - 1):
            a = A(s, e, "all")
            a.flip_bit(test_bit)
            actual = a.get_best_bit(((test_bit + 1)**e))
            expected = test_bit
            self.assertEqual(actual, expected)

    def test_get_best_bit__nebbif(self):
        """
        negative_exactly_best_bit_is_free
        """
        s = 5
        e = 2
        for test_bit in range(s - 1):
            a = A(s, e, "none")
            a.flip_bit(test_bit)
            actual = a.get_best_bit(-((test_bit + 1)**e))
            expected = test_bit
            self.assertEqual(actual, expected)

    def test_get_best_bit__pllbbif(self):
        """
        positive_little_lower_best_bit_is_free
        """
        s = 5
        e = 2
        for test_bit in range(s - 1):
            a = A(s, e, "all")
            a.flip_bit(test_bit)
            actual = a.get_best_bit(((test_bit + 1)**e) - 1)
            expected = test_bit
            self.assertEqual(actual, expected)

    def test_get_best_bit__nllbbif(self):
        """
        negative_little_lower_best_bit_is_free
        """
        s = 5
        e = 2
        for test_bit in range(s - 1):
            a = A(s, e, "none")
            a.flip_bit(test_bit)
            actual = a.get_best_bit(-((test_bit + 1)**e) - 1)
            expected = test_bit
            self.assertEqual(actual, expected)

    def test_get_best_bit__pnebbif(self):
        """
        positive_not_exactly_best_bit_is_free
        """
        s = 5
        e = 2
        for test_bit in range(s - 1):
            a = A(s, e, "all")
            expected = test_bit + (1 if test_bit < 3 else -1)
            a.flip_bit(expected)
            actual = a.get_best_bit(((test_bit + 1)**e))
            self.assertEqual(actual, expected)

    def test_get_best_bit__nnebbif(self):
        """
        negative_not_exactly_best_bit_is_free
        """
        s = 5
        e = 2
        for test_bit in range(s - 1):
            a = A(s, e, "none")
            expected = test_bit + (1 if test_bit < 3 else -1)
            a.flip_bit(expected)
            actual = a.get_best_bit(-((test_bit + 1)**e))
            self.assertEqual(actual, expected)

    def test_flip_all(self):
        s = 5
        e = 2
        a = A(s, e)
        self.assertEqual(a.vec, BitVector(bitlist=[1, 1, 1, 1]))
        self.assertEqual(a.val, 1 + 4 + 9 + 16)
        self.assertEqual(a.bits_set, 4)
        a.flip_all()
        self.assertEqual(a.vec, BitVector(bitlist=[0, 0, 0, 0]))
        self.assertEqual(a.val, 0)
        self.assertEqual(a.bits_set, 0)
        a.flip_bit(1)
        self.assertEqual(a.vec, BitVector(bitlist=[0, 1, 0, 0]))
        self.assertEqual(a.val, 4)
        self.assertEqual(a.bits_set, 1)
        a.flip_all()
        self.assertEqual(a.vec, BitVector(bitlist=[1, 0, 1, 1]))
        self.assertEqual(a.val, 1 + 9 + 16)
        self.assertEqual(a.bits_set, 3)
