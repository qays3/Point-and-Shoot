import httpx
import re

PATTERNS = [
    ("AWS Access Key",     r"AKIA[0-9A-Z]{16}"),
    ("AWS Secret Key",     r"(?i)aws.{0,20}secret.{0,20}['\"][0-9a-zA-Z/+]{40}['\"]"),
    ("Stripe Secret Key",  r"sk_live_[0-9a-zA-Z]{24,}"),
    ("Stripe Public Key",  r"pk_live_[0-9a-zA-Z]{24,}"),
    ("JWT Token",          r"eyJ[a-zA-Z0-9_-]+\.[a-zA-Z0-9_-]+\.[a-zA-Z0-9_-]+"),
    ("Google API Key",     r"AIza[0-9A-Za-z\-_]{35}"),
    ("Private Key Block",  r"-----BEGIN (RSA |EC )?PRIVATE KEY-----"),
    ("Basic Auth in URL",  r"https?://[^:]+:[^@]+@"),
    ("Generic Secret",     r"(?i)(secret|password|passwd|api_key|apikey|token)['\"]?\s*[:=]\s*['\"][^'\"]{8,}['\"]"),
]

JS_PATHS = ["", "/", "/static/bundle.js", "/static/main.js", "/app.js", "/bundle.js", "/main.js"]

async def run(target: str) -> dict:
    logs = []
    findings = []
    base = target.rstrip("/")

    logs.append({"type": "info", "text": f"[+] Secret Sniffer scanning JS/HTML on {base}..."})

    async with httpx.AsyncClient(timeout=10, follow_redirects=True) as client:
        for path in JS_PATHS:
            url = base + path
            try:
                r = await client.get(url)
                if r.status_code != 200:
                    continue

                content_type = r.headers.get("content-type", "")
                if not any(ct in content_type for ct in ["javascript", "html", "text"]):
                    continue

                text = r.text
                logs.append({"type": "info", "text": f"[+] Scanning {url}..."})

                for name, pattern in PATTERNS:
                    matches = re.findall(pattern, text)
                    if matches:
                        logs.append({"type": "danger", "text": f"[!!!] {name} found in {url}"})
                        findings.append({
                            "severity": "high",
                            "title": f"{name} exposed in {path or '/'}",
                            "engine": "Secret Sniffer",
                            "description": f"Regex pattern matched {name} in {url}. Credentials may be exposed.",
                            "url": url,
                            "method": "GET",
                            "remediation": "Revoke the exposed credential immediately. Move all secrets to environment variables or a secrets manager."
                        })

            except Exception:
                pass

    if not findings:
        logs.append({"type": "neutral", "text": "[+] No secrets found in scanned files"})

    return {"logs": logs, "findings": findings}