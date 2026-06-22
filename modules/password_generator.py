import secrets
import string

from modules.utils import load_wordlist


def generate_random_password(
    length=12,
    use_lower=True,
    use_upper=True,
    use_digits=True,
    use_special=True,
    exclude_similar=False,
):
    """
    Generates a cryptographically secure random password.
    """
    if length < 4:
        length = 4  # Minimum viable length for logic

    lower_chars = string.ascii_lowercase
    upper_chars = string.ascii_uppercase
    digit_chars = string.digits
    special_chars = string.punctuation

    # Remove similar characters (o, O, 0, i, I, l, 1, |, l)
    if exclude_similar:
        similar = "oO0iIl1|L"
        lower_chars = "".join([c for c in lower_chars if c not in similar])
        upper_chars = "".join([c for c in upper_chars if c not in similar])
        digit_chars = "".join([c for c in digit_chars if c not in similar])
        special_chars = "".join([c for c in special_chars if c not in similar])

    pool = ""
    guaranteed = []

    if use_lower:
        pool += lower_chars
        guaranteed.append(secrets.choice(lower_chars))
    if use_upper:
        pool += upper_chars
        guaranteed.append(secrets.choice(upper_chars))
    if use_digits:
        pool += digit_chars
        guaranteed.append(secrets.choice(digit_chars))
    if use_special:
        pool += special_chars
        guaranteed.append(secrets.choice(special_chars))

    if not pool:
        # Fallback to standard alphanumeric if nothing is checked
        pool = string.ascii_lowercase + string.digits
        guaranteed.append(secrets.choice(string.ascii_lowercase))
        guaranteed.append(secrets.choice(string.digits))

    # Fill remaining password length with random choices from the pool
    remaining_length = length - len(guaranteed)
    password_chars = guaranteed + [
        secrets.choice(pool) for _ in range(remaining_length)
    ]

    # Shuffle the resulting character list securely
    secrets.SystemRandom().shuffle(password_chars)

    return "".join(password_chars)


def generate_passphrase(
    word_count=4, separator="-", capitalize="title", include_number=True
):
    """
    Generates a memorable passphrase from lists of English words, colors, animals, and nouns.
    """
    # Load words
    words = load_wordlist("passphrase_words.txt")

    # If no wordlist found, try building from colors, animals, and nouns
    if not words:
        colors = load_wordlist("colors.txt")
        animals = load_wordlist("animals.txt")
        nouns = load_wordlist("nouns.txt")
        words = colors + animals + nouns

    # Ultimate fallback if datasets are totally missing
    if not words:
        words = [
            "correct",
            "horse",
            "battery",
            "staple",
            "secure",
            "pass",
            "intelligent",
            "system",
            "cyber",
        ]

    selected_words = [secrets.choice(words) for _ in range(word_count)]

    # Capitalization logic
    if capitalize == "title":
        selected_words = [w.capitalize() for w in selected_words]
    elif capitalize == "upper":
        selected_words = [w.upper() for w in selected_words]
    elif capitalize == "lower":
        selected_words = [w.lower() for w in selected_words]

    passphrase = separator.join(selected_words)

    # Append a random digit if requested
    if include_number:
        passphrase += f"{separator}{secrets.randbelow(100)}"

    return passphrase
