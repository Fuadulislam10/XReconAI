def run_active_scan(target: str, config: dict) -> list:
    """
    Active scanning is disabled by default.
    Keep this module as a controlled expansion point.
    """
    return [{
        "type": "informational",
        "vulnerability": "Active scan module is enabled but not implemented",
        "endpoint": target,
        "evidence": "Implement controlled active checks here (rate-limited, scope-validated).",
        "cwe": "",
        "source": "active_scan",
        "tool_confidence": "low"
    }]

