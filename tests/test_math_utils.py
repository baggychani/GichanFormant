# tests/test_math_utils.py
"""math_utils 정규화·변환 함수 단위 테스트."""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import unittest
import pandas as pd
import numpy as np
from utils.math_utils import (
    hz_to_linear,
    hz_to_bark,
    bark_to_hz,
    hz_to_log,
    calc_f2_prime,
    lobanov_normalization,
    gerstman_normalization,
    nearey1_normalization,
    bigham_normalization,
)


class TestScaleConversion(unittest.TestCase):
    def test_hz_to_linear(self):
        self.assertEqual(hz_to_linear(500), 500)
        self.assertEqual(hz_to_linear(0), 0)

    def test_hz_to_bark(self):
        self.assertGreater(hz_to_bark(1000), 0)
        self.assertTrue(np.isfinite(hz_to_bark(0.1)))
        x = hz_to_bark(np.array([100, 500, 1000]))
        self.assertEqual(len(x), 3)
        self.assertTrue(np.all(np.isfinite(x)))

    def test_bark_to_hz(self):
        x = bark_to_hz(np.array([0, 5, 10]))
        self.assertEqual(len(x), 3)
        self.assertTrue(np.all(np.isfinite(x)))

    def test_hz_to_log(self):
        self.assertAlmostEqual(hz_to_log(100), 2.0, places=5)
        x = hz_to_log(np.array([0.1, 1, 10]))
        self.assertTrue(np.all(np.isfinite(x)))

    def test_calc_f2_prime(self):
        f1 = np.array([300, 400])
        f2 = np.array([2000, 1800])
        f3 = np.array([2500, 2200])
        out = calc_f2_prime(f1, f2, f3)
        self.assertEqual(len(out), 2)
        self.assertTrue(np.all(out >= f2))
        self.assertTrue(np.all(out <= f3))


class TestNormalization(unittest.TestCase):
    def setUp(self):
        self.sample_df = pd.DataFrame(
            {
                "F1": [300, 500, 700],
                "F2": [2000, 1800, 1200],
                "F3": [2500, 2400, 2300],
                "Label": ["i", "e", "a"],
            }
        )

    def test_lobanov(self):
        out = lobanov_normalization(self.sample_df)
        self.assertIn("F1", out.columns)
        self.assertIn("F2", out.columns)
        self.assertEqual(len(out), len(self.sample_df))
        self.assertAlmostEqual(out["F1"].mean(), 0, places=10)
        self.assertAlmostEqual(out["F2"].mean(), 0, places=10)

    def test_gerstman(self):
        out = gerstman_normalization(self.sample_df)
        self.assertEqual(out["F1"].min(), 0)
        self.assertEqual(out["F1"].max(), 999)
        self.assertEqual(out["F2"].min(), 0)
        self.assertEqual(out["F2"].max(), 999)

    def test_nearey1(self):
        out = nearey1_normalization(self.sample_df)
        self.assertIn("F1", out.columns)
        self.assertTrue(np.all(np.isfinite(out["F1"])))

    def test_bigham(self):
        out = bigham_normalization(self.sample_df)
        self.assertIn("F1", out.columns)
        self.assertIn("F2", out.columns)
        self.assertEqual(len(out), len(self.sample_df))


if __name__ == "__main__":
    unittest.main()
