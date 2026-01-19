import requests

def run_passive_recon(target: str, config: dict) -> list:
    """
    Passive-only recon:
    - HTTP headers
    - basic TLS/redirect observation via requests
    NOTE: Keep it lightweight for bug bounty.
    """
    results = []
    timeout = config.get("recon", {}).get("passive", {}).get("timeout_seconds", 10)

    # Try HTTPS first, then HTTP
    urls = [f"https://{target}", f"http://{target}"]

    for url in urls:
        try:
            r = requests.get(url, timeout=timeout, allow_redirects=True, headers={"User-Agent": "XReconAI/Passive"})
            # headers finding
            results.append({
                "type": "informational",
                "vulnerability": "HTTP Response Headers Collected",
                "endpoint": r.url,
                "evidence": str(dict(r.headers))[:2000],
                "cwe": "",
                "source": "passive_recon",
                "tool_confidence": "high"
            })

            # security.txt
            sec_url = r.url.rstrip("/") + "/.well-known/security.txt"
            try:
                s = requests.get(sec_url, timeout=timeout, allow_redirects=True, headers={"User-Agent": "XReconAI/Passive"})
                if s.status_code == 200 and len(s.text.strip()) > 0:
                    results.append({
                        "type": "informational",
                        "vulnerability": "security.txt Found",
                        "endpoint": sec_url,
                        "evidence": s.text[:2000],
                        "cwe": "",
                        "source": "passive_recon",
                        "tool_confidence": "medium"
                    })
            except Exception:
                pass

            # robots.txt
            rob_url = r.url.rstrip("/") + "/robots.txt"
            try:
                rb = requests.get(rob_url, timeout=timeout, allow_redirects=True, headers={"User-Agent": "XReconAI/Passive"})
                if rb.status_code == 200 and len(rb.text.strip()) > 0:
                    results.append({
                        "type": "informational",
                        "vulnerability": "robots.txt Found",
                        "endpoint": rob_url,
                        "evidence": rb.text[:2000],
                        "cwe": "",
                        "source": "passive_recon",
                        "tool_confidence": "medium"
                    })
            except Exception:
                pass

            # if HTTPS works, we can stop after first success
            break

        except Exception as e:
            results.append({
                "type": "informational",
                "vulnerability": "Host Reachability Check Failed",
                "endpoint": url,
                "evidence": str(e),
                "cwe": "",
                "source": "passive_recon",
                "tool_confidence": "low"
            })
            continue

    return results

