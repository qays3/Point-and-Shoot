document.addEventListener('DOMContentLoaded', () => {
    const path = window.location.pathname.replace(/\/$/, '');
    const page = path.split('/').pop();

    if (page === 'dashboard' || page === 'dashboard.html') {
        if (typeof DashboardController !== 'undefined') {
            DashboardController.init();
        }
    }

    if (page === 'report' || page === 'report.html') {
        if (typeof ReportController !== 'undefined') {
            ReportController.init();
        }
    }
});