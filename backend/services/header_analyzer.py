import httpx

REQUIRED_HEADERS = [
    ("strict-transport-security", "high",
     "Missing HSTS Header",
     "Strict-Transport-Security header is absent, leaving connections open to downgrade attacks.",
     "Add: Strict-Transport-Security: max-age=31536000; includeSubDomains; preload"),

    ("x-frame-options", "med",
     "Missing X-Frame-Options",
     "Without X-Frame-Options, the page may be embedded in iframes enabling clickjacking.",
     "Add: X-Frame-Options: DENY or SAMEORIGIN"),

    ("x-content-type-options", "med",
     "Missing X-Content-Type-Options",
     "Browser may MIME-sniff responses, enabling certain XSS attacks.",
     "Add: X-Content-Type-Options: nosniff"),

    ("content-security-policy", "med",
     "Missing Content-Security-Policy",
     "No CSP defined. XSS attacks have a wider attack surface.",
     "Define a Content-Security-Policy header appropriate to your application."),

    ("referrer-policy", "low",
     "Missing Referrer-Policy",
     "Without a Referrer-Policy, sensitive URLs may leak in the Referer header.",
     "Add: Referrer-Policy: strict-origin-when-cross-origin"),

    ("permissions-policy", "low",
     "Missing Permissions-Policy",
     "Browser features like camera and microphone are not restricted.",
     "Add a Permissions-Policy header to restrict unneeded browser features."),
]

async def run(target: str) -> dict:
    logs = []
    findings = []

    logs.append({"type": "info", "text": f"[+] Header Analyzer on {target}..."})

    try:
        async with httpx.AsyncClient(timeout=10, follow_redirects=True) as client:
            r = await client.get(target)
            headers = {k.lower(): v for k, v in r.headers.items()}

            for header, severity, title, description, remediation in REQUIRED_HEADERS:
                if header in headers:
                    logs.append({"type": "info", "text": f"[+] {header}: {headers[header][:60]}"})
                else:
                    logs.append({"type": "warn", "text": f"[!] Missing: {header}"})
                    findings.append({
                        "severity": severity,
                        "title": title,
                        "engine": "Header Analyzer",
                        "description": description,
                        "url": target,
                        "method": "GET",
                        "remediation": remediation
                    })

    except Exception as e:
        logs.append({"type": "warn", "text": f"[!] Header analysis error: {str(e)}"})

    return {"logs": logs, "findings": findings}