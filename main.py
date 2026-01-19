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


def apply_cli_overrides(config: dict, args) -> dict:
    # config file override with CLI options
    if args.target:
        config.setdefault("target", {})
        config["target"]["primary_domain"] = args.target

    if args.passive_only is not None:
        config.setdefault("project", {})
        config["project"]["passive_only"] = args.passive_only

    if args.active is not None:
        config.setdefault("scan", {}).setdefault("active", {})
        config["scan"]["active"]["enabled"] = args.active

    if args.confidence is not None:
        config.setdefault("ai", {}).setdefault("confidence_threshold", {})
        config["ai"]["confidence_threshold"]["report_only_if_above"] = args.confidence

    return config


def main():
    parser = argparse.ArgumentParser(description="XReconAI - AI-Powered Security Reconnaissance & Analysis")
    parser.add_argument("--config", default="config.yaml", help="Path to config.yaml")
    parser.add_argument("--target", help="Target domain (overrides config.yaml)")
    parser.add_argument("--passive-only", dest="passive_only", action="store_true", help="Force passive-only mode")
    parser.add_argument("--no-passive-only", dest="passive_only", action="store_false", help="Disable passive-only mode")
    parser.set_defaults(passive_only=None)

    parser.add_argument("--active", dest="active", action="store_true", help="Enable active scanning (authorized only)")
    parser.add_argument("--no-active", dest="active", action="store_false", help="Disable active scanning")
    parser.set_defaults(active=None)

    parser.add_argument("--confidence", type=int, help="AI confidence threshold (0-100) for reporting")
    args = parser.parse_args()

    print("\n[+] Starting XReconAI...\n")

    # Load + override
    config = load_config(args.config)
    config = apply_cli_overrides(config, args)

    target = config["target"]["primary_domain"]
    print(f"[+] Target: {target}")

    # Scope validation
    print("[+] Validating scope...")
    if not validate_scope(target, config):
        print("[!] Target is out of scope. Aborting.")
        sys.exit(1)
    print("[+] Scope validation passed.")

    # Passive recon
    print("[+] Running passive reconnaissance...")
    passive_results = run_passive_recon(target, config)
    all_findings = passive_results

    # Active scan (optional)
    if not config["project"].get("passive_only", True):
        if config.get("scan", {}).get("active", {}).get("enabled", False):
            print("[+] Running active scanning...")
            active_results = run_active_scan(target, config)
            all_findings.extend(active_results)

    # Correlate
    print("[+] Correlating findings...")
    normalized_findings = correlate_findings(all_findings)
    if not normalized_findings:
        print("[+] No meaningful findings detected.")
        sys.exit(0)

    # AI analysis
    print("[+] Running AI analysis...")
    ai_results = run_ai_analysis(normalized_findings, config)

    # Risk scoring
    print("[+] Calculating risk scores...")
    scored = [calculate_risk(f, config) for f in ai_results]

    # Report
    print("[+] Generating report...")
    generate_report(scored, config)

    print("\n[✓] XReconAI completed successfully.\n")


if __name__ == "__main__":
    main()
