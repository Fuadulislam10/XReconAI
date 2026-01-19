def correlate_findings(raw_findings: list) -> list:
    """
    Convert raw recon/scan outputs into normalized finding objects.
    Expect raw_findings = list[dict]. Return list[dict].
    """
    normalized = []
    seen = set()

    for f in raw_findings or []:
        if not isinstance(f, dict):
            continue

        vuln = (f.get("vulnerability") or f.get("type") or "informational").strip()
        endpoint = (f.get("endpoint") or f.get("url") or "").strip()
        evidence = (f.get("evidence") or f.get("details") or "").strip()
        cwe = (f.get("cwe") or "").strip()

        key = (vuln.lower(), endpoint.lower(), evidence[:120].lower())
        if key in seen:
            continue
        seen.add(key)

        normalized.append({
            "vulnerability": vuln,
            "endpoint": endpoint,
            "parameter": f.get("parameter"),
            "evidence": evidence,
            "cwe": cwe,
            "source": f.get("source", "xreconai"),
            "tool_confidence": f.get("tool_confidence", "unknown")
        })

    return normalized

