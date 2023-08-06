# -*- coding: utf-8 -*-
""" Test primitive operations """

import unittest

from commonutil_fileio_persistentqueue.textfolder import cmp_serial
from commonutil_fileio_persistentqueue.textfolder import compute_p2m16

SERIAL_TEST_ARTIFACT_1 = [
		(0, 0xFFF000),
		(0, 0xFFFFFF),
		(1, 0xFFF001),
		(0x000FFF, 0xFFFFFF),
		(0xFFEFFF, 0),
		(0xFFEFFF, 0),
		(0xFFF000, 0xFFEFFF),
		(0xFFF002, 0xFFF001),
		(0xFFF003, 0xFFF002),
		(1, 0),
		(3, 1),
		(0x1000, 7),
]


class Test_TextFolder_Serial(unittest.TestCase):
	"""
	Test serial operations
	"""

	def test_cmp_gt_1(self):
		for a, b in SERIAL_TEST_ARTIFACT_1:
			self.assertGreater(cmp_serial(a, b), 0, "%06X vs. %06X" % (a, b))

	def test_cmp_lt_1(self):
		for a, b in SERIAL_TEST_ARTIFACT_1:
			self.assertLess(cmp_serial(b, a), 0, "%06X vs. %06X" % (b, a))

	def test_cmp_eq_1(self):
		for a, b in SERIAL_TEST_ARTIFACT_1:
			self.assertEqual(cmp_serial(a, a), 0, "%06X vs. %06X" % (a, a))
			self.assertEqual(cmp_serial(b, b), 0, "%06X vs. %06X" % (b, b))


P2M16_TEST_ARTIFACT_1 = [
		(1, 1),
		(2, 1),
		(3, 2),
		(4, 2),
		(5, 3),
		(7, 3),
		(8, 3),
		(9, 4),
		(16, 4),
		(64, 6),
		(65, 7),
]


class Test_TextFolder_P2M16(unittest.TestCase):
	"""
	Test power-of-2 caculation (max-16)
	"""

	def test_1(self):
		for v, p in P2M16_TEST_ARTIFACT_1:
			self.assertEqual(compute_p2m16(v), p, "%d in 2^ %d" % (v, p))
