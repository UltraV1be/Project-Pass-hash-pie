
from modules.utils import load_wordlist_set, load_wordlist

# Lazy loading of datasets
_common_passwords = None
_keyboard_patterns = None
_sequential_patterns = None


def get_common_passwords():
    global _common_passwords
    if _common_passwords is None:
        _common_passwords = load_wordlist_set("common_passwords.txt")
    return _common_passwords


def get_keyboard_patterns():
    global _keyboard_patterns
    if _keyboard_patterns is None:
        _keyboard_patterns = load_wordlist("keyboard_patterns.txt")
    return _keyboard_patterns


def get_sequential_patterns():
    global _sequential_patterns
    if _sequential_patterns is None:
        _sequential_patterns = load_wordlist("sequential_patterns.txt")
    return _sequential_patterns


def detect_pattern_substring(password, patterns, min_length=3):
    """
    Checks if the password contains a substring of a pattern of at least `min_length` size.
    Returns the matching pattern if found.
    """
    pwd = password.lower()
    if len(pwd) < min_length:
        return None

    for pattern in patterns:
        pat_len = len(pattern)
        # Check window sizes from len(pwd) down to min_length
        for w_size in range(min_length, min(len(pwd), pat_len) + 1):
            for i in range(len(pwd) - w_size + 1):
                sub = pwd[i : i + w_size]
                if sub in pattern:
                    return sub
    return None


def calculate_strength(password):
    """
    Evaluates password complexity, returns a score (0-100), rating, and list of warnings.
    """
    score = 0
    warnings = []

    if not password:
        return {
            "score": 0,
            "rating": "Very Weak",
            "warnings": ["Password is empty"],
            "details": {
                "length": 0,
                "has_lowercase": False,
                "has_uppercase": False,
                "has_digits": False,
                "has_special": False,
                "in_dictionary": False,
                "has_sequential": False,
                "has_keyboard_pattern": False,
            },
        }

    length = len(password)

    # 1. Dictionary Check
    in_dictionary = password.lower() in get_common_passwords()
    if in_dictionary:
        warnings.append(
            "This is a highly common password and can be cracked instantly."
        )
        score = min(score, 10)  # Heavy penalty for common passwords

    # 2. Basic Character Class Analysis
    has_lowercase = any(c.islower() for c in password)
    has_uppercase = any(c.isupper() for c in password)
    has_digits = any(c.isdigit() for c in password)
    has_special = any(not c.isalnum() for c in password)

    # 3. Base Score Calculations (if not in dictionary)
    if not in_dictionary:
        # Length contribution: up to 40 points
        if length >= 16:
            score += 40
        elif length >= 12:
            score += 30
        elif length >= 8:
            score += 20
        elif length >= 6:
            score += 10
        else:
            score += 5
            warnings.append(
                "Password is too short. Use at least 8 characters (12+ recommended)."
            )

        # Diversity contribution: up to 40 points
        diversity_count = sum(
            [has_lowercase, has_uppercase, has_digits, has_special]
        )
        score += diversity_count * 10

        if diversity_count < 3:
            warnings.append(
                "Include a mix of uppercase, lowercase, numbers, and symbols."
            )

        # Bonus for extra length (>12 chars) with good diversity
        if length > 12 and diversity_count >= 3:
            score += 10

        # Deduct for sequential pattern matches
        seq_match = detect_pattern_substring(
            password, get_sequential_patterns(), min_length=3
        )
        if seq_match:
            score -= 15
            warnings.append(f"Contains sequential characters: '{seq_match}'.")
            has_sequential = True
        else:
            has_sequential = False

        # Deduct for keyboard patterns (e.g. qwerty)
        kb_match = detect_pattern_substring(
            password, get_keyboard_patterns(), min_length=3
        )
        if kb_match:
            score -= 15
            warnings.append(f"Contains keyboard sequence: '{kb_match}'.")
            has_keyboard_pattern = True
        else:
            has_keyboard_pattern = False

        # Deduct for simple repeat patterns (e.g., 'aaaa' or '1111')
        has_repeats = False
        for i in range(len(password) - 2):
            if password[i] == password[i + 1] == password[i + 2]:
                has_repeats = True
                break
        if has_repeats:
            score -= 10
            warnings.append(
                "Avoid repeating the same character consecutive times (e.g., 'aaa')."
            )

    else:
        has_sequential = (
            detect_pattern_substring(
                password, get_sequential_patterns(), min_length=3
            )
            is not None
        )
        has_keyboard_pattern = (
            detect_pattern_substring(
                password, get_keyboard_patterns(), min_length=3
            )
            is not None
        )

    # Cap score boundaries [0, 100]
    score = max(0, min(100, score))

    # Rating Tier Assignment
    if score >= 80:
        rating = "Very Secure"
    elif score >= 60:
        rating = "Strong"
    elif score >= 40:
        rating = "Moderate"
    elif score >= 20:
        rating = "Weak"
    else:
        rating = "Very Weak"

    return {
        "score": score,
        "rating": rating,
        "warnings": warnings,
        "details": {
            "length": length,
            "has_lowercase": has_lowercase,
            "has_uppercase": has_uppercase,
            "has_digits": has_digits,
            "has_special": has_special,
            "in_dictionary": in_dictionary,
            "has_sequential": has_sequential,
            "has_keyboard_pattern": has_keyboard_pattern,
        },
    }
