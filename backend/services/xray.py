import httpx

OUTDATED = {
    "nginx": ["1.14", "1.15", "1.16", "1.10", "1.12"],
    "apache": ["2.2", "2.3"],
    "php": ["5.", "7.0", "7.1", "7.2", "7.3"],
    "iis": ["6.0", "7.0", "7.5"],
}

async def run(target: str) -> dict:
    logs = []
    findings = []

    logs.append({"type": "info", "text": f"[+] Tech Stack X-Ray on {target}..."})

    try:
        async with httpx.AsyncClient(timeout=10, follow_redirects=True) as client:
            r = await client.get(target)
            headers = dict(r.headers)

            interesting = ["server", "x-powered-by", "x-aspnet-version", "x-generator", "via"]
            for h in interesting:
                if h in headers:
                    val = headers[h]
                    logs.append({"type": "info", "text": f"[+] {h}: {val}"})

                    for tech, versions in OUTDATED.items():
                        if tech in val.lower():
                            for v in versions:
                                if v in val:
                                    findings.append({
                                        "severity": "low",
                                        "title": f"Outdated {tech.upper()} version: {val}",
                                        "engine": "Tech Stack X-Ray",
                                        "description": f"Header {h} reveals outdated software: {val}",
                                        "url": target,
                                        "method": "GET",
                                        "remediation": f"Upgrade {tech} to the latest stable release and suppress version disclosure."
                                    })

            if "server" not in headers:
                logs.append({"type": "neutral", "text": "[+] Server header not present"})

    except Exception as e:
        logs.append({"type": "warn", "text": f"[!] X-Ray error: {str(e)}"})

    return {"logs": logs, "findings": findings}