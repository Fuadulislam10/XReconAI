import os
from datetime import datetime

def generate_report(findings: list, config: dict) -> None:
    out_dir = config.get("report", {}).get("output_dir", "reports/output")
    os.makedirs(out_dir, exist_ok=True)

    ts = datetime.utcnow().strftime("%Y%m%d-%H%M%S")
    path = os.path.join(out_dir, f"xreconai-report-{ts}.md")

    lines = []
    lines.append(f"# XReconAI Report\n")
    lines.append(f"- Project: {config.get('project', {}).get('name','XReconAI')}\n")
    lines.append(f"- Version: {config.get('project', {}).get('version','')}\n")
    lines.append(f"- Target: {config.get('target', {}).get('primary_domain','')}\n")
    lines.append(f"- Generated: {datetime.utcnow().isoformat()}Z\n")
    lines.append("\n---\n")

    ready = [f for f in findings if f.get("status") == "ready"]
    lowc  = [f for f in findings if f.get("status") != "ready"]

    lines.append(f"## Summary\n")
    lines.append(f"- Total findings: {len(findings)}\n")
    lines.append(f"- Reported (meets confidence threshold): {len(ready)}\n")
    lines.append(f"- Not reported (low confidence): {len(lowc)}\n")

    def render_item(idx, f):
        risk = f.get("risk", {})
        ai = f.get("ai", {})
        lines.append(f"\n### {idx}. {f.get('vulnerability','')}\n")
        lines.append(f"- Endpoint: `{f.get('endpoint','')}`\n")
        if f.get("parameter"):
            lines.append(f"- Parameter: `{f.get('parameter')}`\n")
        lines.append(f"- Severity: **{risk.get('severity','')}**  | Priority: **{risk.get('priority','')}**\n")
        lines.append(f"- AI Confidence: **{risk.get('confidence',0)}%**  | Likelihood: **{ai.get('likelihood','')}**\n")
        lines.append(f"- Impact: {ai.get('impact','')}\n")
        lines.append(f"- Reasoning: {ai.get('reasoning','')}\n")
        if f.get("evidence"):
            lines.append("\n**Evidence (truncated):**\n")
            lines.append("```text\n" + (f.get("evidence","")[:1200]) + "\n```\n")

    lines.append("\n## Findings\n")
    if not ready:
        lines.append("\n_No findings met the confidence threshold. Review raw outputs manually._\n")
    else:
        for i, f in enumerate(ready, 1):
            render_item(i, f)

    if lowc:
        lines.append("\n---\n## Low Confidence / Informational\n")
        for i, f in enumerate(lowc, 1):
            render_item(i, f)

    lines.append("\n---\n## Legal Disclaimer\n")
    lines.append("XReconAI is intended for authorized security testing and educational purposes only. "
                 "Do not test systems you do not own or have explicit permission to test.\n")

    with open(path, "w", encoding="utf-8") as fp:
        fp.write("\n".join(lines))

    print(f"[+] Report saved: {path}")

