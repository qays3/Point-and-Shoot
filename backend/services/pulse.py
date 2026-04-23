import httpx

async def run(target: str) -> dict:
    logs = []
    findings = []

    logs.append({"type": "info", "text": f"[+] Pulse check on {target}..."})

    try:
        async with httpx.AsyncClient(timeout=10, follow_redirects=True) as client:
            r = await client.get(target)
            code = r.status_code
            server = r.headers.get("server", "unknown")
            logs.append({"type": "info", "text": f"[+] {target} -> LIVE ({code}) server={server}"})

            if code >= 500:
                findings.append({
                    "severity": "med",
                    "title": f"Server error {code} on {target}",
                    "engine": "Pulse Checker",
                    "description": f"Target returned HTTP {code} indicating a server-side error.",
                    "url": target,
                    "method": "GET",
                    "remediation": "Investigate server logs and fix the underlying error."
                })
    except httpx.ConnectTimeout:
        logs.append({"type": "warn", "text": f"[!] {target} -> DEAD (timeout)"})
    except Exception as e:
        logs.append({"type": "warn", "text": f"[!] Pulse error: {str(e)}"})

    return {"logs": logs, "findings": findings}