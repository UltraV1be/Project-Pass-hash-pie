import sys
import os

# Adjust sys.path to find main modules
sys.path.insert(0, os.path.abspath(os.path.dirname(os.path.dirname(__file__))))

from modules.password_generator import (
    generate_random_password,
    generate_passphrase,
)


def test_generate_random_length():
    pwd = generate_random_password(length=20)
    assert len(pwd) == 20


def test_generate_random_char_classes():
    # Only lowercase and digits
    pwd = generate_random_password(
        length=30,
        use_lower=True,
        use_upper=False,
        use_digits=True,
        use_special=False,
    )
    for char in pwd:
        assert char.islower() or char.isdigit()


def test_generate_passphrase_format():
    phrase = generate_passphrase(
        word_count=3, separator="*", include_number=False
    )
    parts = phrase.split("*")
    assert len(parts) == 3
