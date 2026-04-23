const ReportController = (() => {
    function init() {
        const scan = ScanModel.get();

        if (!scan || !scan.target || scan.findings.length === 0) {
            return;
        }

        const report = ReportModel.fromScan(scan);
        ReportView.render(report);
    }

    return { init };
})();