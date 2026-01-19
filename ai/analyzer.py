from ai.prompts import prompt_validate_finding

def run_ai_analysis(findings: list, config: dict) -> list:
    """
    This is a READY pipeline with a SAFE fallback.
    If you later connect OpenAI, replace the stub section with a real client call.
    """
    ai_enabled = config.get("ai", {}).get("enabled", True)
    if not ai_enabled:
        # no AI: return findings as-is
        return findings

    analyzed = []
    for f in findings:
        # ---- STUB / FALLBACK (No API call) ----
        # Simple heuristic: informational findings get lower confidence
        vuln = (f.get("vulnerability") or "").lower()
        if "found" in vuln or "collected" in vuln or "informational" in vuln:
            confidence = 55
            likelihood = "Low"
            impact = "Informational"
            reasoning = "Passive recon output; not a confirmed vulnerability."
        else:
            confidence = 70
            likelihood = "Medium"
            impact = "Potential security concern; needs manual verification."
            reasoning = "Heuristic-based triage (no live exploitation)."

        f["ai"] = {
            "prompt_preview": prompt_validate_finding(f)[:600],
            "likelihood": likelihood,
            "confidence": confidence,
            "impact": impact,
            "reasoning": reasoning,
        }
        analyzed.append(f)

    return analyzed

