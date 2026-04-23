const DashboardController = (() => {
    let _scanning = false;
    let _enginesDone = 0;

    function init() {
        ToggleView.init(null);
        const btn   = document.getElementById('scanBtn');
        const input = document.getElementById('targetInput');
        if (btn)   btn.addEventListener('click', _onScanClick);
        if (input) input.addEventListener('keydown', e => { if (e.key === 'Enter') _onScanClick(); });
    }

    function _onScanClick() {
        if (_scanning) { _abort(); return; }
        const input = document.getElementById('targetInput');
        const target = input ? input.value.trim() : '';
        if (!target) {
            input.focus();
            input.style.borderColor = 'var(--error-primary)';
            setTimeout(() => { input.style.borderColor = ''; }, 1500);
            return;
        }
        _startScan(target);
    }

    function _startScan(target) {
        _scanning = true;
        _enginesDone = 0;
        const enabled = ToggleView.getEnabled();
        if (enabled.length === 0) return;

        ScanModel.start(target);
        ToggleView.setDisabled(true);
        DashboardView.setStatus('running');
        DashboardView.setScanBtn(true);
        DashboardView.setProgress(1, 'Starting scan...');
        TerminalView.clear();
        TerminalView.setActive(true);

        API.runScan(target, enabled, {
            onLog: (log) => {
                ScanModel.addLog(log);
                TerminalView.appendLine(log);
            },
            onFinding: (finding) => {
                ScanModel.addFinding(finding);
                DashboardView.addFinding(finding);
                DashboardView.updateStats(ScanModel.get().findings);
            },
            onEngineStatus: (engine, status) => {
                ScanModel.setEngineStatus(engine, status);
                DashboardView.setEngineStatus(engine, status);
                if (status === 'done') {
                    _enginesDone++;
                    DashboardView.updateEngineCount(_enginesDone, enabled.length);
                }
            },
            onProgress: (pct, label) => {
                ScanModel.setProgress(pct, label);
                DashboardView.setProgress(pct, label);
            },
            onDone: (findings) => {
                _finishScan();
            },
            onError: (msg) => {
                TerminalView.appendLine({ type: 'danger', text: '[!!!] Error: ' + msg });
                _abort();
            }
        });
    }

    function _finishScan() {
        _scanning = false;
        ScanModel.finish();
        ToggleView.setDisabled(false);
        DashboardView.setStatus('done');
        DashboardView.setScanBtn(false);
        DashboardView.setProgress(100, 'Scan complete');
        TerminalView.appendLine({ type: 'info', text: '[+] Done. View full report in the Report tab.' });
        TerminalView.setActive(false);
    }

    function _abort() {
        _scanning = false;
        DashboardView.setStatus('idle');
        DashboardView.setScanBtn(false);
        DashboardView.setProgress(0, '');
        TerminalView.setActive(false);
        ToggleView.setDisabled(false);
    }

    return { init };
})();