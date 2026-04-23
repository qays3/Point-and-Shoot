const ScanModel = (() => {
    const STORAGE_KEY = 'pas_scan';

    const defaultState = () => ({
        id: null,
        target: '',
        status: 'idle',
        startedAt: null,
        finishedAt: null,
        enabledEngines: ['subdomain','pulse','dns','xray','idor','dirfinder','secrets','cors','headers'],
        engineStatus: {
            subdomain: 'idle',
            pulse: 'idle',
            dns: 'idle',
            xray: 'idle',
            idor: 'idle',
            dirfinder: 'idle',
            secrets: 'idle',
            cors: 'idle',
            headers: 'idle'
        },
        progress: 0,
        logs: [],
        findings: []
    });

    let state = defaultState();

    function save() {
        try {
            sessionStorage.setItem(STORAGE_KEY, JSON.stringify(state));
        } catch (_) {}
    }

    function load() {
        try {
            const raw = sessionStorage.getItem(STORAGE_KEY);
            if (raw) state = JSON.parse(raw);
        } catch (_) {
            state = defaultState();
        }
    }

    function get() {
        return state;
    }

    function reset() {
        state = defaultState();
        save();
    }

    function setTarget(url) {
        state.target = url;
    }

    function setStatus(s) {
        state.status = s;
        save();
    }

    function setEngineStatus(engine, status) {
        state.engineStatus[engine] = status;
        save();
    }

    function setProgress(pct, label) {
        state.progress = pct;
        state.progressLabel = label || '';
        save();
    }

    function addLog(entry) {
        state.logs.push(entry);
        save();
    }

    function addFinding(finding) {
        state.findings.push(finding);
        save();
    }

    function setEnabledEngines(list) {
        state.enabledEngines = list;
    }

    function start(target) {
        state = defaultState();
        state.id = Date.now();
        state.target = target;
        state.status = 'running';
        state.startedAt = new Date().toISOString();
        save();
    }

    function finish() {
        state.status = 'done';
        state.finishedAt = new Date().toISOString();
        save();
    }

    load();

    return { get, reset, setTarget, setStatus, setEngineStatus, setProgress, addLog, addFinding, setEnabledEngines, start, finish, load };
})();