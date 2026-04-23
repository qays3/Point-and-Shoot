const ReportView = (() => {
    function render(report) {
        _setMeta(report);
        _setStats(report.stats);
        _renderFindings(report.findings);
        _initFilters(report);
        _initExport(report);
    }

    function _setMeta(report) {
        const target = document.getElementById('metaTarget');
        const date   = document.getElementById('metaDate');
        const dur    = document.getElementById('metaDuration');
        if (target) target.textContent = report.target || '—';
        if (date)   date.textContent = report.startedAt ? new Date(report.startedAt).toLocaleString() : '—';
        if (dur)    dur.textContent = report.duration || '—';
    }

    function _setStats(stats) {
        const map = { statTotal: stats.total, statHigh: stats.high, statMed: stats.med, statLow: stats.low, statEngines: stats.engines };
        Object.entries(map).forEach(([id, val]) => {
            const el = document.getElementById(id);
            if (el) el.textContent = val;
        });
    }

    function _renderFindings(findings) {
        const list = document.getElementById('findingsList');
        if (!list) return;
        list.innerHTML = '';

        if (!findings || findings.length === 0) {
            list.innerHTML = '<div class="report-empty"><p class="report-empty-text">No findings match this filter.</p></div>';
            return;
        }

        findings.forEach((f, i) => {
            const card = document.createElement('div');
            card.className = 'finding-card sev-' + f.severity;
            card.style.animationDelay = (i * 0.04) + 's';
            card.innerHTML =
                '<div class="finding-card-head">' +
                    '<span class="badge badge-' + f.severity + '">' + f.severity.toUpperCase() + '</span>' +
                    '<span class="finding-card-title">' + _esc(f.title) + '</span>' +
                    '<span class="finding-card-engine">' + _esc(f.engine) + '</span>' +
                    '<span class="finding-chevron"><svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polyline points="6 9 12 15 18 9"/></svg></span>' +
                '</div>' +
                '<div class="finding-card-body">' +
                    '<div class="finding-detail-grid">' +
                        '<div><div class="finding-detail-label">Description</div><div class="finding-detail-value">' + _esc(f.description) + '</div></div>' +
                        '<div><div class="finding-detail-label">Endpoint</div><div class="finding-detail-value">' + _esc(f.url) + '</div></div>' +
                    '</div>' +
                    '<div class="finding-remediation">' +
                        '<div class="finding-remediation-label">Remediation</div>' +
                        '<div class="finding-remediation-text">' + _esc(f.remediation) + '</div>' +
                    '</div>' +
                '</div>';

            card.querySelector('.finding-card-head').addEventListener('click', () => {
                card.classList.toggle('expanded');
            });

            list.appendChild(card);
        });
    }

    function _initFilters(report) {
        document.querySelectorAll('[data-filter]').forEach(btn => {
            btn.addEventListener('click', () => {
                document.querySelectorAll('[data-filter]').forEach(b => b.classList.remove('active'));
                btn.classList.add('active');
                _renderFindings(ReportModel.filter(report, btn.dataset.filter));
            });
        });
    }

    function _initExport(report) {
        const btn = document.getElementById('btnExportJson');
        if (!btn) return;
        btn.addEventListener('click', () => {
            const blob = new Blob([ReportModel.toJson(report)], { type: 'application/json' });
            const url  = URL.createObjectURL(blob);
            const a    = document.createElement('a');
            a.href = url;
            a.download = 'pas-report-' + (report.scanId || Date.now()) + '.json';
            a.click();
            URL.revokeObjectURL(url);
        });
    }

    function _esc(str) {
        const d = document.createElement('div');
        d.textContent = str || '';
        return d.innerHTML;
    }

    return { render };
})();