import httpx

ORIGINS = [
    "https://evil.com",
    "https://attacker.com",
    "null",
    "https://sub.evil.com",
]

async def run(target: str) -> dict:
    logs = []
    findings = []

    logs.append({"type": "info", "text": f"[+] CORS Interrogator testing {target}..."})

    async with httpx.AsyncClient(timeout=10, follow_redirects=True) as client:
        for origin in ORIGINS:
            try:
                headers = {"Origin": origin}
                r = await client.options(target, headers=headers)
                acao = r.headers.get("access-control-allow-origin", "")
                acac = r.headers.get("access-control-allow-credentials", "")

                logs.append({"type": "info", "text": f"[+] Origin: {origin} -> ACAO: {acao or 'not set'}"})

                if acao == "*":
                    findings.append({
                        "severity": "med",
                        "title": "Wildcard CORS: Access-Control-Allow-Origin: *",
                        "engine": "CORS Interrogator",
                        "description": "Server allows all origins. Any website can read responses from this API.",
                        "url": target,
                        "method": "OPTIONS",
                        "remediation": "Replace wildcard with an explicit allowlist of trusted origins."
                    })

                elif acao == origin:
                    severity = "high" if acac.lower() == "true" else "med"
                    logs.append({"type": "danger" if severity == "high" else "warn",
                                 "text": f"[!!!] CORS reflects {origin} (credentials={acac})"})
                    findings.append({
                        "severity": severity,
                        "title": f"CORS misconfiguration: reflects {origin}",
                        "engine": "CORS Interrogator",
                        "description": f"Server reflects attacker origin {origin} with credentials={acac}.",
                        "url": target,
                        "method": "OPTIONS",
                        "remediation": "Validate the Origin header against a strict allowlist. Never reflect arbitrary origins."
                    })

            except Exception:
                pass

    if not findings:
        logs.append({"type": "neutral", "text": "[+] No CORS misconfigurations found"})

    return {"logs": logs, "findings": findings}