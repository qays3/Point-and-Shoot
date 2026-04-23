const DashboardView = (() => {
    function setStatus(state) {
        const dot  = document.getElementById('statusDot');
        const text = document.getElementById('statusText');
        if (dot)  dot.className = 'status-dot ' + state;
        if (text) text.textContent = state.charAt(0).toUpperCase() + state.slice(1);
    }

    function setScanBtn(scanning) {
        const btn = document.getElementById('scanBtn');
        if (!btn) return;
        if (scanning) {
            btn.innerHTML = '<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><rect x="6" y="6" width="12" height="12"/></svg> Stop';
            btn.classList.add('scanning');
        } else {
            btn.innerHTML = '<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polygon points="5 3 19 12 5 21 5 3"/></svg> Scan Now';
            btn.classList.remove('scanning');
        }
    }

    function setProgress(pct, label) {
        const wrapper = document.getElementById('progressWrapper');
        const fill    = document.getElementById('progressFill');
        const lbl     = document.getElementById('progressLabel');
        const pctEl   = document.getElementById('progressPct');
        if (!wrapper) return;
        wrapper.style.display = pct > 0 ? 'block' : 'none';
        if (fill)  fill.style.width = pct + '%';
        if (lbl)   lbl.textContent = label || '';
        if (pctEl) pctEl.textContent = pct + '%';
    }

    function setEngineStatus(engine, status) {
        const item = document.querySelector('[data-engine-status="' + engine + '"]');
        if (!item) return;
        item.className = 'engine-chip ' + status;
        const dot = item.querySelector('.status-dot');
        if (dot) dot.className = 'status-dot ' + status;
    }

    function updateStats(findings) {
        const high = findings.filter(f => f.severity === 'high').length;
        const med  = findings.filter(f => f.severity === 'med').length;
        const low  = findings.filter(f => f.severity === 'low').length;
        const eH = document.getElementById('statHigh');
        const eM = document.getElementById('statMed');
        const eL = document.getElementById('statLow');
        if (eH) eH.textContent = high;
        if (eM) eM.textContent = med;
        if (eL) eL.textContent = low;
    }

    function updateEngineCount(done, total) {
        const el = document.getElementById('statEngines');
        if (el) el.textContent = done + '/' + total;
    }

    function addFinding(finding) {
        const body = document.getElementById('intelligenceBody');
        if (!body) return;
        const empty = body.querySelector('.empty-state');
        if (empty) empty.remove();

        const dot = document.getElementById('reportDot');
        if (dot) { dot.classList.remove('inactive'); dot.classList.add('active'); }

        const row = document.createElement('div');
        row.className = 'finding-row';
        row.innerHTML =
            '<span class="badge badge-' + finding.severity + '">' + finding.severity.toUpperCase() + '</span>' +
            '<span class="finding-text">' + _esc(finding.title) + '</span>';
        body.appendChild(row);
        body.scrollTop = body.scrollHeight;
    }

    function _esc(str) {
        const d = document.createElement('div');
        d.textContent = str;
        return d.innerHTML;
    }

    return { setStatus, setScanBtn, setProgress, setEngineStatus, updateStats, addFinding, updateEngineCount };
})();