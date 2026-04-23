const ReportModel = (() => {
    function fromScan(scan) {
        const findings = scan.findings || [];
        return {
            target: scan.target,
            scanId: scan.id,
            startedAt: scan.startedAt,
            finishedAt: scan.finishedAt,
            duration: _duration(scan.startedAt, scan.finishedAt),
            findings,
            stats: {
                total: findings.length,
                high:  findings.filter(f => f.severity === 'high').length,
                med:   findings.filter(f => f.severity === 'med').length,
                low:   findings.filter(f => f.severity === 'low').length,
                engines: Object.values(scan.engineStatus).filter(s => s === 'done').length
            }
        };
    }

    function filter(report, severity) {
        if (severity === 'all') return report.findings;
        return report.findings.filter(f => f.severity === severity);
    }

    function toJson(report) {
        return JSON.stringify(report, null, 2);
    }

    function _duration(start, end) {
        if (!start || !end) return '--';
        const ms = new Date(end) - new Date(start);
        const s = Math.floor(ms / 1000);
        if (s < 60) return s + 's';
        return Math.floor(s / 60) + 'm ' + (s % 60) + 's';
    }

    return { fromScan, filter, toJson };
})();