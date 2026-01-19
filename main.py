import yaml
import sys
from core.scope_validator import validate_scope
from recon.passive import run_passive_recon
from recon.active import run_active_scan
from core.correlator import correlate_findings
from ai.analyzer import run_ai_analysis
from core.risk_engine import calculate_risk
from ai.reporter import generate_report


def load_config(path="config.yaml"):
    try:
        with open(path, "r") as f:
            return yaml.safe_load(f)
    except Exception as e:
        print(f"[!] Failed to load config: {e}")
        sys.exit(1)


def main():
    print("\n[+] Starting XReconAI...\n")

    # 1️⃣ Load config
    config = load_config()

    target = config["target"]["primary_domain"]
    print(f"[+] Target: {target}")

    # 2️⃣ Scope & legal validation
    print("[+] Validating scope...")
    if not validate_scope(target, config):
        print("[!] Target is out of scope. Aborting.")
        sys.exit(1)

    print("[+] Scope validation passed.")

    # 3️⃣ Passive Recon (Always safe)
    print("[+] Running passive reconnaissance...")
    passive_results = run_passive_recon(target, config)

    all_findings = passive_results

    # 4️⃣ Active Scan (Only if allowed)
    if not config["project"].get("passive_only", True):
        if config["scan"]["active"]["enabled"]:
            print("[+] Running active scanning...")
            active_results = run_active_scan(target, config)
            all_findings.extend(active_results)

    # 5️⃣ Normalize & correlate findings
    print("[+] Correlating findings...")
    normalized_findings = correlate_findings(all_findings)

    if not normalized_findings:
        print("[+] No meaningful findings detected.")
        sys.exit(0)

    # 6️⃣ AI analysis pipeline
    print("[+] Running AI analysis...")
    ai_results = run_ai_analysis(normalized_findings, config)

    # 7️⃣ Risk scoring
    print("[+] Calculating risk scores...")
    scored_findings = []
    for finding in ai_results:
        scored = calculate_risk(finding, config)
        scored_findings.append(scored)

    # 8️⃣ Generate report
    print("[+] Generating report...")
    generate_report(scored_findings, config)

    print("\n[✓] XReconAI completed successfully.\n")


if __name__ == "__main__":
    main()
