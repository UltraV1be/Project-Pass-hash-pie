import json


class ExportService:
    """
    Handles formatting and preparation of reports for file downloads.
    """

    @classmethod
    def export_to_json(cls, analysis_results):
        """
        Formats results as indented JSON.
        """
        # Remove raw password for security if it is present
        sanitized_results = analysis_results.copy()
        if "password" in sanitized_results:
            del sanitized_results["password"]

        return json.dumps(sanitized_results, indent=4)

    @classmethod
    def export_to_text(cls, password, analysis_results):
        """
        Formats results as a clean, human-readable text report.
        """
        # Obfuscate password in report header (e.g. p***word)
        obfuscated = (
            password[0] + "*" * (len(password) - 2) + password[-1]
            if len(password) > 2
            else "*" * len(password)
        )

        strength = analysis_results.get("strength", {})
        entropy = analysis_results.get("entropy", {})
        crack_times = analysis_results.get("crack_times", {})
        risk = analysis_results.get("risk", {})
        suggestions = analysis_results.get("suggestions", [])
        ai_advice = analysis_results.get("ai_advice", "")

        report = []
        report.append("==================================================")
        report.append("       SECUREPASS-INTELLIGENCE SECURITY REPORT     ")
        report.append("==================================================")
        report.append(f"Password Assessed:  {obfuscated}")
        report.append(f"Password Length:    {len(password)} characters")
        report.append(
            f"Security Rating:    {strength.get('rating', 'N/A')} (Score: {strength.get('score', 0)}/100)"
        )
        report.append(
            f"Shannon Entropy:    {entropy.get('entropy', 0.0)} bits (Pool Size: {entropy.get('pool_size', 0)})"
        )
        report.append(f"Overall Risk Level: {risk.get('risk_level', 'N/A')}")
        report.append(
            f"Public Breaches:    {analysis_results.get('breach_count', 0)} leaks detected"
        )
        report.append("--------------------------------------------------")
        report.append("CRACK TIME ESTIMATION")
        report.append(
            f"- Online Attack:         {crack_times.get('online_readable')}"
        )
        report.append(
            f"- Offline Fast Hashing:  {crack_times.get('offline_fast_readable')}"
        )
        report.append(
            f"- Offline Slow Hashing:  {crack_times.get('offline_slow_readable')}"
        )
        report.append("--------------------------------------------------")
        report.append("EXPERT RISKS DETECTED")
        if risk.get("reasons"):
            for reason in risk.get("reasons"):
                report.append(f"- {reason}")
        else:
            report.append("- No immediate risks identified.")
        report.append("--------------------------------------------------")
        report.append("ACTIONABLE SECURITY CHECKLIST")
        for suggestion in suggestions:
            report.append(f"[ ] {suggestion}")
        report.append("--------------------------------------------------")
        report.append("AI CYBERSECURITY ADVISORY")
        report.append(ai_advice)
        report.append("==================================================")
        report.append(
            "Disclaimer: This security assessment is based on mathematical entropy models and public"
        )
        report.append(
            "compromised registries. It is not an absolute proof of safety."
        )

        return "\n".join(report)
