def generate_suggestions(strength_details, entropy_details, breach_count):
    """
    Generates a list of actionable suggestions to improve the password's strength.
    """
    suggestions = []

    # 1. Breach check suggestions
    if breach_count > 0:
        suggestions.append(
            "CRITICAL: Change this password immediately. It has been leaked in public breaches and is compromised."
        )
        suggestions.append(
            "Use a unique, randomized password or passphrase that you have never used before."
        )
        return suggestions  # Primary directive is replacement

    # 2. General strength checks
    details = strength_details.get("details", {})
    length = details.get("length", 0)
    in_dictionary = details.get("in_dictionary", False)

    if in_dictionary:
        suggestions.append(
            "Do not use common words, phrases, or names. These are standard in dictionary attack lists."
        )
        suggestions.append(
            "Consider generating a multi-word passphrase (e.g., 'Crimson-Falcon-Jumps') for memorable strength."
        )

    # Length suggestions
    if length < 8:
        suggestions.append(
            "Increase length to at least 12 characters. Longer passwords exponentially increase search spaces for offline attacks."
        )
    elif length < 12:
        suggestions.append(
            "Add 4 more characters. Passwords with 12+ characters are significantly harder to brute force."
        )

    # Character diversity suggestions
    if not details.get("has_uppercase", False):
        suggestions.append(
            "Insert at least one uppercase letter (A-Z) to widen the character pool."
        )
    if not details.get("has_lowercase", False):
        suggestions.append("Insert at least one lowercase letter (a-z).")
    if not details.get("has_digits", False):
        suggestions.append("Include at least one digit (0-9).")
    if not details.get("has_special", False):
        suggestions.append(
            "Incorporate special symbols (e.g., @, #, $, %, !, &) to make the password highly complex."
        )

    # Pattern suggestions
    if details.get("has_sequential", False):
        suggestions.append(
            "Remove character sequences like '123' or 'abc' which are easily predicted by brute force tools."
        )
    if details.get("has_keyboard_pattern", False):
        suggestions.append(
            "Avoid keyboard tracks or rows (e.g. 'qwerty', 'asdf')."
        )

    # If the password is secure, give positive reinforcement
    if not suggestions and strength_details.get("score", 0) >= 80:
        suggestions.append(
            "Excellent password! Keep using unique passwords for every online account."
        )
        suggestions.append(
            "Consider enabling Multi-Factor Authentication (MFA) on accounts using this password for additional security."
        )

    return suggestions
