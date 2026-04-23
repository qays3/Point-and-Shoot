import httpx

async def run(target: str) -> dict:
    host = target.replace("https://", "").replace("http://", "").strip("/").split("/")[0]
    logs = []
    findings = []

    logs.append({"type": "info", "text": f"[+] Querying crt.sh for subdomains of {host}..."})

    try:
        async with httpx.AsyncClient(timeout=15) as client:
            r = await client.get(f"https://crt.sh/?q=%25.{host}&output=json")
            data = r.json()
            names = sorted(set(
                entry["name_value"].strip().lstrip("*.")
                for entry in data
                if "name_value" in entry
            ))

        if names:
            logs.append({"type": "info", "text": f"[+] Found {len(names)} subdomains: {', '.join(names[:5])}"})
            for name in names:
                if name != host:
                    findings.append({
                        "severity": "low",
                        "title": f"Subdomain discovered: {name}",
                        "engine": "Subdomain Enumerator",
                        "description": f"Subdomain {name} found via certificate transparency logs.",
                        "url": name,
                        "method": "CT",
                        "remediation": "Review exposed subdomains and disable any unused or sensitive services."
                    })
        else:
            logs.append({"type": "neutral", "text": f"[+] No subdomains found for {host}"})

    except Exception as e:
        logs.append({"type": "warn", "text": f"[!] Subdomain enum error: {str(e)}"})

    return {"logs": logs, "findings": findings}