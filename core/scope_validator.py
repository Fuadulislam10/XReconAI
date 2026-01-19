import fnmatch
from pathlib import Path

def _read_scope_file(scope_path: str):
    p = Path(scope_path)
    if not p.exists():
        return []
    lines = []
    for raw in p.read_text(encoding="utf-8").splitlines():
        s = raw.strip()
        if not s or s.startswith("#"):
            continue
        lines.append(s)
    return lines

def _matches_scope(target: str, pattern: str) -> bool:
    # supports exact "example.com" and wildcard "*.example.com"
    # normalize common patterns
    target = target.strip().lower()
    pattern = pattern.strip().lower()

    if pattern.startswith("*."):
        # fnmatch works for *.example.com
        return fnmatch.fnmatch(target, pattern)
    return target == pattern

def validate_scope(target: str, config: dict) -> bool:
    legal = config.get("legal", {})
    if not legal.get("require_scope_validation", True):
        return True

    scope_file = config.get("target", {}).get("scope_file", "scope.txt")
    out_of_scope = set([x.lower() for x in config.get("target", {}).get("out_of_scope", [])])

    if target.lower() in out_of_scope:
        return False

    patterns = _read_scope_file(scope_file)
    if not patterns:
        # if no scope file, be safe
        return False

    for pat in patterns:
        if _matches_scope(target, pat):
            return True

    return False

