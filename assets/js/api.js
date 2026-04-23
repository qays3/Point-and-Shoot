const API = (() => {
    const BASE = "";

    async function createScan(target, engines) {
        const r = await fetch(`${BASE}/api/scan`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ target, engines }),
        });
        if (!r.ok) throw new Error("Failed to create scan");
        return r.json();
    }

    async function getReport(scanId) {
        const r = await fetch(`${BASE}/api/report/${scanId}`);
        if (!r.ok) throw new Error("Failed to fetch report");
        return r.json();
    }

    function runScan(target, enabledEngines, callbacks) {
        const { onLog, onFinding, onEngineStatus, onProgress, onDone, onError } = callbacks;

        createScan(target, enabledEngines).then(scan => {
            const protocol = location.protocol === "https:" ? "wss" : "ws";
            const ws = new WebSocket(`${protocol}://${location.host}/ws/scan/${scan.id}`);

            ws.onmessage = (event) => {
                const msg = JSON.parse(event.data);

                if (msg.type === "log")      onLog(msg.log);
                if (msg.type === "finding")  onFinding(msg.finding);
                if (msg.type === "engine")   onEngineStatus(msg.engine, msg.status);
                if (msg.type === "progress") onProgress(msg.pct, msg.label);
                if (msg.type === "status" && msg.status === "done") {
                    getReport(scan.id).then(report => onDone(report.findings));
                }
                if (msg.type === "error") {
                    if (onError) onError(msg.message);
                }
            };

            ws.onerror = () => {
                if (onError) onError("WebSocket connection failed");
            };
        }).catch(err => {
            if (onError) onError(err.message);
        });
    }

    return { runScan, getReport };
})();