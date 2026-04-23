const ToggleView = (() => {
    function init(onChange) {
        const deck = document.getElementById('toggleDeck');
        if (!deck) return;

        deck.querySelectorAll('.toggle-btn').forEach(btn => {
            btn.addEventListener('click', () => {
                btn.classList.toggle('active');
                const active = _getActive();
                if (onChange) onChange(active);
            });
        });
    }

    function _getActive() {
        const deck = document.getElementById('toggleDeck');
        if (!deck) return [];
        return Array.from(deck.querySelectorAll('.toggle-btn.active'))
            .map(b => b.dataset.engine);
    }

    function getEnabled() {
        return _getActive();
    }

    function setDisabled(disabled) {
        const deck = document.getElementById('toggleDeck');
        if (!deck) return;
        deck.querySelectorAll('.toggle-btn').forEach(btn => {
            btn.disabled = disabled;
            btn.style.opacity = disabled ? '0.5' : '';
            btn.style.cursor = disabled ? 'not-allowed' : '';
        });
    }

    return { init, getEnabled, setDisabled };
})();