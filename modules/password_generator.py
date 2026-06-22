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


def generate_keyword_password(
    keyword="password",
    length=16,
    leetspeak=True,
    include_numbers=True,
    include_special=True
):
    """
    Generates a strong password based on a user-provided keyword.
    """
    if not keyword:
        keyword = "cyber"

    base_word = keyword
    if leetspeak:
        replacements = {'a': '@', 'e': '3', 'i': '1', 'o': '0', 's': '$', 't': '7', 'A': '@', 'E': '3', 'I': '1', 'O': '0', 'S': '$', 'T': '7'}
        new_word = ""
        for char in base_word:
            if char in replacements and secrets.choice([True, False]):
                new_word += replacements[char]
            else:
                new_word += char
        base_word = new_word

    pool = string.ascii_letters
    if include_numbers:
        pool += string.digits
    if include_special:
        pool += string.punctuation

    chars_to_add = max(4, length - len(base_word))
    prefix_len = chars_to_add // 2
    suffix_len = chars_to_add - prefix_len

    prefix = "".join(secrets.choice(pool) for _ in range(prefix_len))
    suffix = "".join(secrets.choice(pool) for _ in range(suffix_len))

    return prefix + base_word + suffix
