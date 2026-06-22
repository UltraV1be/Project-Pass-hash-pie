import os
import logging
from config import Config

logger = logging.getLogger(__name__)

# Try to import google-generativeai, handle if not installed
try:
    import google.generativeai as genai

    HAS_GEMINI_SDK = True
except ImportError:
    HAS_GEMINI_SDK = False


def get_rule_based_advice(risk_level, score, breach_count):
    """
    Fallback expert cybersecurity advice based on password analytics.
    """
    if breach_count > 0:
        return (
            "This password has been identified in a public database leak. Continuing to use this password "
            "represents an extreme risk of credential stuffing attacks, where bots try leaked combinations "
            "across multiple services. You should immediately change this password wherever it is in use."
        )

    if risk_level == "Critical" or score < 20:
        return (
            "Your password has severe security vulnerabilities. Attackers using standard brute-force dictionaries "
            "or basic GPU cracking rigs will crack it within seconds. We advise replacing it with a passphrase "
            "composed of 4 or more random words, which combines high system entropy with ease of recall."
        )

    if risk_level == "High":
        return (
            "This password lacks complexity or sufficient length. In cybersecurity, length is the most significant "
            "defense against offline dictionary attacks. We recommend extending it to at least 14 characters and "
            "avoiding standard keyboard sequences or personal identifiers."
        )

    if risk_level == "Medium":
        return (
            "Your password offers moderate protection. While it may resist simple online attacks, it could be "
            "vulnerable to dedicated offline cracking if the service's database is ever compromised. Consider adding "
            "special symbols or numbers to increase the complexity pool."
        )

    return (
        "This is a highly secure password that meets modern cryptographic recommendation guidelines. To maximize "
        "your digital security, ensure this password is never reused across different websites, and consider "
        "storing it in a secure local password manager with Multi-Factor Authentication enabled."
    )


def get_ai_advice(
    password_str, score, rating, entropy, crack_times, risk_level, breach_count
):
    """
    Generates tailored security advice using Gemini if configured, otherwise falls back to expert rules.
    """
    api_key = getattr(Config, "GEMINI_API_KEY", None)

    if not api_key or not HAS_GEMINI_SDK:
        return get_rule_based_advice(risk_level, score, breach_count)

    try:
        genai.configure(api_key=api_key)
        # Using gemini-1.5-flash as the standard efficient model
        model = genai.GenerativeModel("gemini-1.5-flash")

        prompt = (
            f"You are a cybersecurity expert analysis engine. Analyze this password's security metrics:\n"
            f"- Rating: {rating} (Score: {score}/100)\n"
            f"- Shannon Entropy: {entropy} bits\n"
            f"- Est. Crack Time (Offline Fast GPU): {crack_times.get('offline_fast_readable')}\n"
            f"- Risk level: {risk_level}\n"
            f"- Breach count: {breach_count}\n\n"
            f"Provide a concise, direct, 2-3 sentence expert cybersecurity assessment of this password. "
            f"Focus on the primary risk and concrete action. Do not repeat the raw metrics, explain what they mean for the user."
        )

        response = model.generate_content(prompt)
        if response and response.text:
            return response.text.strip()

    except Exception as e:
        logger.error(
            f"Gemini API execution failed, falling back to rule-based advice: {e}"
        )

    return get_rule_based_advice(risk_level, score, breach_count)
