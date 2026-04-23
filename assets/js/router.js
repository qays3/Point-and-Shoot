const Router = (() => {
    const routes = {};

    function on(path, handler) {
        routes[path] = handler;
    }

    function resolve() {
        const path = window.location.pathname.split('/').pop() || 'index.html';
        if (routes[path]) routes[path]();
    }

    window.addEventListener('popstate', resolve);

    return { on, resolve };
})();