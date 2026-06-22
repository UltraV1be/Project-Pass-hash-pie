import math
import string


def calculate_entropy(password):
    """
    Calculates the Shannon entropy of a password: H = L * log2(R)
    where L is password length and R is pool size of character set.
    """
    if not password:
        return {
            "entropy": 0.0,
            "pool_size": 0,
            "length": 0,
            "pool_breakdown": {
                "lowercase": False,
                "uppercase": False,
                "digits": False,
                "special": False,
                "extended": False,
            },
        }

    length = len(password)

    # Track which character categories are present
    has_lowercase = False
    has_uppercase = False
    has_digits = False
    has_special = False
    has_extended = False

    special_chars = set(string.punctuation)

    for char in password:
        if char.islower():
            has_lowercase = True
        elif char.isupper():
            has_uppercase = True
        elif char.isdigit():
            has_digits = True
        elif char in special_chars:
            has_special = True
        else:
            has_extended = True

    # Calculate pool size R
    pool_size = 0
    if has_lowercase:
        pool_size += 26
    if has_uppercase:
        pool_size += 26
    if has_digits:
        pool_size += 10
    if has_special:
        pool_size += 33
    if has_extended:
        pool_size += 100  # Default estimate for extended/unicode characters

    if pool_size == 0:
        entropy = 0.0
    else:
        entropy = length * math.log2(pool_size)

    return {
        "entropy": round(entropy, 2),
        "pool_size": pool_size,
        "length": length,
        "pool_breakdown": {
            "lowercase": has_lowercase,
            "uppercase": has_uppercase,
            "digits": has_digits,
            "special": has_special,
            "extended": has_extended,
        },
    }
