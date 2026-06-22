def evaluate_risk(strength_details, entropy_details, breach_count):
    """
    Evaluates the overall security risk level of a password.
    Returns a dictionary with a risk level ("Low", "Medium", "High", "Critical"),
    a risk score (0-100 where 100 is highest risk), and specific reasons.
    """
    risk_level = "Low"
    risk_score = 0
    reasons = []

    # 1. Breach Check (Critical Risk)
    if breach_count > 0:
        risk_level = "Critical"
        risk_score = 100
        reasons.append(
            f"Compromised: Found in {breach_count:,} public data breaches. It should never be used."
        )

    # 2. Dictionary Check (Critical Risk)
    elif strength_details.get("in_dictionary", False):
        risk_level = "Critical"
        risk_score = 95
        reasons.append(
            "Highly vulnerable: Appears in lists of most common passwords. Easily guessable."
        )

    else:
        # 3. Base calculations on score and entropy
        score = strength_details.get("score", 0)
        entropy = entropy_details.get("entropy", 0.0)

        # Calculate risk score (inverse of strength score, but refined)
        risk_score = 100 - score

        if score < 25 or entropy < 35:
            risk_level = "High"
            reasons.append(
                "Low complexity: Easily crackable due to short length or low character diversity."
            )
        elif score < 55 or entropy < 60:
            risk_level = "Medium"
            reasons.append(
                "Moderate risk: Lacks sufficient length or character diversity for long-term safety."
            )
        else:
            risk_level = "Low"

        # Specific structural risks
        if strength_details.get("has_sequential", False):
            reasons.append(
                "Predictable patterns: Contains sequential character runs."
            )
        if strength_details.get("has_keyboard_pattern", False):
            reasons.append(
                "Predictable patterns: Contains keyboard swipe runs (e.g. 'qwerty')."
            )

        length = strength_details.get("length", 0)
        if length < 8:
            reasons.append(
                "Dangerous length: Passwords shorter than 8 characters can be brute-forced very quickly."
            )

    # Ensure risk score matches the category minimums
    if risk_level == "Critical":
        risk_score = max(risk_score, 90)
    elif risk_level == "High":
        risk_score = max(risk_score, 70)
    elif risk_level == "Medium":
        risk_score = max(30, min(69, risk_score))
    else:
        risk_score = min(29, risk_score)

    return {
        "risk_level": risk_level,
        "risk_score": risk_score,
        "reasons": reasons,
    }
