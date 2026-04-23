import dns.resolver
import dns.exception

async def run(target: str) -> dict:
    host = target.replace("https://", "").replace("http://", "").strip("/").split("/")[0]
    logs = []
    findings = []

    logs.append({"type": "info", "text": f"[+] DNS investigation on {host}..."})

    resolver = dns.resolver.Resolver()
    resolver.timeout = 5
    resolver.lifetime = 5

    for rtype in ["A", "MX", "NS", "TXT"]:
        try:
            answers = resolver.resolve(host, rtype)
            vals = [str(r) for r in answers]
            logs.append({"type": "neutral", "text": f"[+] {rtype}: {', '.join(vals[:3])}"})
        except Exception:
            logs.append({"type": "neutral", "text": f"[+] {rtype}: no record"})

    try:
        txt = resolver.resolve(host, "TXT")
        records = [str(r) for r in txt]
        spf = any("v=spf1" in r for r in records)
        dmarc_host = f"_dmarc.{host}"
        try:
            dmarc_ans = resolver.resolve(dmarc_host, "TXT")
            dmarc = any("v=DMARC1" in str(r) for r in dmarc_ans)
        except Exception:
            dmarc = False

        if not spf:
            logs.append({"type": "warn", "text": f"[!] SPF record missing on {host}"})
            findings.append({
                "severity": "med",
                "title": f"Missing SPF record on {host}",
                "engine": "DNS Investigator",
                "description": "No SPF record found. Allows spoofed emails from this domain.",
                "url": host,
                "method": "DNS",
                "remediation": "Add a TXT record: v=spf1 include:your-provider.com ~all"
            })

        if not dmarc:
            logs.append({"type": "warn", "text": f"[!] DMARC not configured on {host}"})
            findings.append({
                "severity": "med",
                "title": f"Missing DMARC policy on {host}",
                "engine": "DNS Investigator",
                "description": "No DMARC record found. Email spoofing attacks are more likely to succeed.",
                "url": host,
                "method": "DNS",
                "remediation": "Add _dmarc TXT record: v=DMARC1; p=reject; rua=mailto:dmarc@yourdomain.com"
            })

    except Exception:
        pass

    try:
        cname = resolver.resolve(host, "CNAME")
        for r in cname:
            cname_val = str(r)
            logs.append({"type": "warn", "text": f"[!] CNAME {host} -> {cname_val} (check for takeover)"})
            findings.append({
                "severity": "high",
                "title": f"Potential CNAME takeover: {host}",
                "engine": "DNS Investigator",
                "description": f"CNAME points to {cname_val}. If unclaimed, an attacker can take over.",
                "url": host,
                "method": "DNS",
                "remediation": "Verify the CNAME target is claimed and active. Remove dangling records."
            })
    except Exception:
        pass

    return {"logs": logs, "findings": findings}