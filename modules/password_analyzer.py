from modules.entropy_calculator import calculate_entropy
from modules.strength_calculator import calculate_strength
from modules.breach_checker import check_password_breach
from modules.risk_engine import evaluate_risk
from modules.suggestion_engine import generate_suggestions
from modules.ai_advisor import get_ai_advice
from modules.crack_time_estimator import estimate_crack_time


def analyze_password(password, check_breaches=True):
    """
    Orchestrates the complete security assessment of a password, combining complexity checks,
    entropy math, crack time estimates, breach status, risk engines, and AI advisor tips.
    """
    # 1. Calculate entropy details
    entropy_details = calculate_entropy(password)
    entropy_val = entropy_details.get("entropy", 0.0)

    # 2. Estimate crack times
    crack_times = estimate_crack_time(entropy_val)

    # 3. Calculate strength scoring and checks
    strength_details = calculate_strength(password)

    # 4. Check breaches securely (if enabled)
    breach_count = 0
    if check_breaches:
        breach_count = check_password_breach(password)

    # 5. Evaluate overall risk
    risk_details = evaluate_risk(
        strength_details, entropy_details, breach_count
    )

    # 6. Generate improvements checklist
    suggestions = generate_suggestions(
        strength_details, entropy_details, breach_count
    )

    # 7. Query AI advisor
    ai_advice = get_ai_advice(
        password_str=password,
        score=strength_details.get("score", 0),
        rating=strength_details.get("rating", "Very Weak"),
        entropy=entropy_val,
        crack_times=crack_times,
        risk_level=risk_details.get("risk_level", "High"),
        breach_count=breach_count,
    )

    return {
        "password_length": len(password),
        "entropy": entropy_details,
        "crack_times": crack_times,
        "strength": strength_details,
        "breach_count": breach_count,
        "risk": risk_details,
        "suggestions": suggestions,
        "ai_advice": ai_advice,
    }
