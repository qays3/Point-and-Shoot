import httpx

PARAMS = ["id", "user_id", "uid", "account_id", "order_id", "invoice_id"]
FUZZ_VALUES = ["1", "2", "12", "100", "999", "0"]

async def run(target: str) -> dict:
    logs = []
    findings = []

    logs.append({"type": "info", "text": f"[+] IDOR fuzzing on {target}..."})

    try:
        async with httpx.AsyncClient(timeout=10, follow_redirects=True) as client:
            baseline = await client.get(target)
            baseline_len = len(baseline.content)

            for param in PARAMS:
                for val in FUZZ_VALUES:
                    url = f"{target.rstrip('/')}?{param}={val}"
                    try:
                        r = await client.get(url)
                        if r.status_code == 200 and abs(len(r.content) - baseline_len) > 100:
                            logs.append({"type": "danger", "text": f"[!!!] IDOR candidate: {param}={val} returned unique content"})
                            findings.append({
                                "severity": "high",
                                "title": f"Possible IDOR on ?{param}={val}",
                                "engine": "IDOR Hunter",
                                "description": f"Parameter {param}={val} returned a unique response differing from baseline by {abs(len(r.content) - baseline_len)} bytes.",
                                "url": url,
                                "method": "GET",
                                "remediation": "Implement server-side authorization checks. Validate that the authenticated user owns the requested resource."
                            })
                        else:
                            logs.append({"type": "neutral", "text": f"[+] {param}={val} -> {r.status_code}"})
                    except Exception:
                        pass

    except Exception as e:
        logs.append({"type": "warn", "text": f"[!] IDOR error: {str(e)}"})

    return {"logs": logs, "findings": findings}