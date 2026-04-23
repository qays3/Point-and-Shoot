import httpx

WORDLIST = [
    "admin", "login", "dashboard", "api", "backup", "config", "db",
    "debug", "test", "dev", "staging", "old", "uploads", "files",
    "static", "assets", "logs", "tmp", "private", "secret", ".git",
    ".env", "robots.txt", "sitemap.xml", "phpinfo.php", "wp-admin",
    "console", "panel", "manage", "administrator", "user", "users",
]

async def run(target: str) -> dict:
    logs = []
    findings = []
    base = target.rstrip("/")

    logs.append({"type": "info", "text": f"[+] Dir Finder scanning {base} ({len(WORDLIST)} paths)..."})

    try:
        async with httpx.AsyncClient(timeout=8, follow_redirects=False) as client:
            for path in WORDLIST:
                url = f"{base}/{path}"
                try:
                    r = await client.get(url)
                    if r.status_code in [200, 301, 302, 403]:
                        severity = "high" if r.status_code == 200 else "med"
                        logs.append({"type": "warn" if r.status_code != 200 else "danger",
                                     "text": f"[!] /{path} found ({r.status_code})"})
                        findings.append({
                            "severity": severity,
                            "title": f"Exposed path: /{path} ({r.status_code})",
                            "engine": "Directory Finder",
                            "description": f"Path /{path} returned HTTP {r.status_code}.",
                            "url": url,
                            "method": "GET",
                            "remediation": "Restrict access to sensitive paths. Return 404 instead of 403 to avoid path disclosure."
                        })
                except Exception:
                    pass

    except Exception as e:
        logs.append({"type": "warn", "text": f"[!] Dir Finder error: {str(e)}"})

    if not findings:
        logs.append({"type": "neutral", "text": "[+] No exposed directories found"})

    return {"logs": logs, "findings": findings}