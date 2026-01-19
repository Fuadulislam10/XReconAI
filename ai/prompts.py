SYSTEM_PROMPT = """You are XReconAI, an autonomous security analysis engine for legal bug bounty and security research.
You do NOT provide instructions for illegal activity. You ONLY analyze findings and write professional reports.
Be conservative; if unsure, say so.
"""

def prompt_validate_finding(finding: dict) -> str:
    return f"""
Analyze this finding and decide if it's likely a real security issue or informational/noise.

Return STRICT JSON with keys:
- likelihood: Low/Medium/High
- confidence: 0-100
- reasoning: short
- cwe: string or empty
- impact: short

Finding:
{finding}
""".strip()

