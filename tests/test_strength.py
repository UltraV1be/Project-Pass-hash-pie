import sys
import os

# Adjust sys.path to find main modules
sys.path.insert(0, os.path.abspath(os.path.dirname(os.path.dirname(__file__))))

from modules.strength_calculator import calculate_strength


def test_strength_empty():
    res = calculate_strength("")
    assert res["score"] == 0
    assert res["rating"] == "Very Weak"


def test_strength_common_dictionary():
    # 'password' is in common_passwords.txt
    res = calculate_strength("password")
    assert res["details"]["in_dictionary"] is True
    assert res["score"] <= 10
    assert res["rating"] == "Very Weak"


def test_strength_sequential():
    # 'abcd' is sequential
    res = calculate_strength("StrongPass123!")
    # Should flag sequential since '123' is a digit sequence
    assert res["details"]["has_sequential"] is True
