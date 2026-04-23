const TerminalView = (() => {
    function _el() { return document.getElementById('terminalBody'); }

    function clear() {
        const el = _el();
        if (el) el.innerHTML = '';
    }

    function appendLine(log) {
        const el = _el();
        if (!el) return;
        const empty = el.querySelector('.empty-state');
        if (empty) empty.remove();

        const line = document.createElement('div');
        line.className = 'term-line ' + (log.type || 'neutral');
        line.textContent = log.text;
        el.appendChild(line);
        el.scrollTop = el.scrollHeight;
    }

    function setActive(active) {
        const dot = document.getElementById('termDot');
        if (!dot) return;
        if (active) { dot.classList.remove('inactive'); dot.classList.add('active'); }
        else        { dot.classList.remove('active'); dot.classList.add('inactive'); }
    }

    return { clear, appendLine, setActive };
})();