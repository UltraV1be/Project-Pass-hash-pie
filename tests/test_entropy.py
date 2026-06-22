import sys
import os

# Adjust sys.path to find main modules
sys.path.insert(0, os.path.abspath(os.path.dirname(os.path.dirname(__file__))))

from modules.entropy_calculator import calculate_entropy


def test_entropy_empty():
    res = calculate_entropy("")
    assert res["entropy"] == 0.0
    assert res["length"] == 0
    assert res["pool_size"] == 0


def test_entropy_lowercase():
    res = calculate_entropy("abc")
    assert res["length"] == 3
    assert res["pool_size"] == 26
    # 3 * log2(26) = 3 * 4.7004 = 14.1
    assert res["entropy"] == 14.1


def test_entropy_complex():
    res = calculate_entropy("aA1!")
    # Contains lowercase (26), uppercase (26), digit (10), special (33) -> pool = 95
    assert res["pool_size"] == 95
    assert res["length"] == 4
    # 4 * log2(95) = 4 * 6.57 = 26.28
    assert res["entropy"] == 26.28
