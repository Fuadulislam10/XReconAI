def calculate_risk(finding: dict, config: dict) -> dict:
    """
    Hybrid risk scoring: uses AI confidence (if present) + simple severity mapping.
    """
    vuln = (finding.get("vulnerability") or "").lower()
    ai_conf = int(finding.get("ai", {}).get("confidence", 0) or 0)

    # simple heuristic severity baseline
    if any(x in vuln for x in ["rce", "remote code", "sql injection", "sqli"]):
        severity = "Critical"
        priority = "P1"
    elif any(x in vuln for x in ["xss", "idor", "auth bypass", "ssrf"]):
        severity = "High"
        priority = "P2"
    elif any(x in vuln for x in ["open redirect", "misconfig", "information"]):
        severity = "Medium"
        priority = "P3"
    else:
        severity = "Low"
        priority = "P4"

    # adjust by confidence
    threshold = config.get("ai", {}).get("confidence_threshold", {}).get("report_only_if_above", 65)
    if ai_conf and ai_conf < threshold:
        finding["status"] = "unconfirmed_low_confidence"
    else:
        finding["status"] = "ready"

    finding["risk"] = {
        "severity": severity,
        "priority": priority,
        "confidence": ai_conf
    }
    return finding

