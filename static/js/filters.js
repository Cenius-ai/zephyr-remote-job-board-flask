/* ================================================================
   Zephyr — Filters JavaScript (AJAX progressive enhancement)
   ================================================================ */

(function () {
    'use strict';

    var form = document.getElementById('filter-form');
    if (!form) return;

    // AJAX filtering: intercept form submit and filter in-place
    form.addEventListener('submit', function (e) {
        e.preventDefault();

        var params = new URLSearchParams(new FormData(form));

        // Push filter state into the URL without full reload
        var newUrl = window.location.pathname + '?' + params.toString();
        window.history.pushState({}, '', newUrl);

        fetchAndRender(params);
    }, { passive: false });

    // Handle back/forward navigation
    window.addEventListener('popstate', function () {
        var qs = window.location.search;
        var params = new URLSearchParams(qs);
        fetchAndRender(params);
    });

    function showSpinner() {
        var section = document.querySelector('.results-section');
        if (!section) return;

        section.innerHTML =
            '<div class="spinner-overlay">' +
            '<div class="spinner" aria-hidden="true"></div>' +
            '<p class="spinner-label">Loading jobs…</p>' +
            '</div>';
    }

    function showError(message) {
        var section = document.querySelector('.results-section');
        if (!section) return;

        section.innerHTML =
            '<div class="empty-state">' +
            '<svg width="64" height="64" viewBox="0 0 24 24" fill="none" stroke="var(--danger)" stroke-width="1.5" aria-hidden="true">' +
            '<circle cx="12" cy="12" r="10"/>' +
            '<line x1="12" y1="8" x2="12" y2="12"/>' +
            '<line x1="12" y1="16" x2="12.01" y2="16"/>' +
            '</svg>' +
            '<h2>Something went wrong</h2>' +
            '<p>' + (message || 'Unable to load jobs. Please try again.') + '</p>' +
            '</div>';
    }

    function fetchAndRender(params) {
        var resultsSection = document.querySelector('.results-section');
        if (!resultsSection) return;

        showSpinner();

        var apiUrl = '/api/jobs?' + params.toString();

        fetch(apiUrl)
            .then(function (resp) {
                if (!resp.ok) throw new Error('Server error: ' + resp.status);
                return resp.json();
            })
            .then(function (data) {
                renderResults(data, params);
            })
            .catch(function (err) {
                console.error('Filter error:', err);
                showError('Unable to load jobs. Please check your connection and try again.');
            });
    }

    function renderResults(data, params) {
        var section = document.querySelector('.results-section');
        if (!section) return;

        var html = '';

        // Header with count
        html += '<div class="results-header">';
        html += '<p class="results-count">';
        if (data.total === 0) {
            html += 'No jobs match your filters. Try broadening your search.';
        } else if (data.total === 1) {
            html += '1 job found';
        } else {
            html += data.total + ' jobs found';
        }
        html += '</p></div>';

        if (data.jobs && data.jobs.length > 0) {
            html += '<div class="job-grid">';
            data.jobs.forEach(function (job) {
                html += renderJobCard(job);
            });
            html += '</div>';

            // Pagination
            if (data.pages > 1) {
                html += renderPagination(data, params);
            }
        } else {
            html += '<div class="empty-state">';
            html += '<svg width="64" height="64" viewBox="0 0 24 24" fill="none" stroke="var(--muted)" stroke-width="1.5" aria-hidden="true"><circle cx="11" cy="11" r="8"/><line x1="21" y1="21" x2="16.65" y2="16.65"/></svg>';
            html += '<h2>No jobs found</h2>';
            html += '<p>Try adjusting your filters or <a href="/">viewing all listings</a>.</p>';
            html += '</div>';
        }

        section.innerHTML = html;
    }

    function renderJobCard(job) {
        var card = '<article class="job-card">';
        card += '<div class="job-card-header">';
        card += '<div class="company-avatar">' + escapeHtml(job.company[0]) + '</div>';
        card += '<div class="job-card-meta">';
        card += '<h2 class="job-card-title"><a href="/jobs/' + job.id + '" class="job-card-link">' + escapeHtml(job.title) + '</a></h2>';
        card += '<p class="job-card-company">' + escapeHtml(job.company) + '</p>';
        card += '</div>';
        card += '<span class="remote-badge remote-badge--' + job.remote_type + '">' + capitalize(job.remote_type) + '</span>';
        card += '</div>';

        if (job.tags && job.tags.length > 0) {
            card += '<div class="job-card-tags">';
            var shownTags = job.tags.slice(0, 5);
            shownTags.forEach(function (t) {
                card += '<span class="tag-pill">' + escapeHtml(t) + '</span>';
            });
            if (job.tags.length > 5) {
                card += '<span class="tag-pill tag-pill--more">+' + (job.tags.length - 5) + '</span>';
            }
            card += '</div>';
        }

        card += '<div class="job-card-footer">';
        if (job.salary_min && job.salary_max) {
            card += '<span class="salary">$' + fmtNum(job.salary_min) + ' – $' + fmtNum(job.salary_max) + '</span>';
        } else if (job.salary_min) {
            card += '<span class="salary">From $' + fmtNum(job.salary_min) + '</span>';
        } else {
            card += '<span class="salary salary--undisclosed">Salary undisclosed</span>';
        }
        card += '<span class="posted-date">' + job.posted_date + '</span>';
        card += '</div>';
        card += '</article>';
        return card;
    }

    function renderPagination(data, params) {
        var nav = '<nav class="pagination">';
        if (data.page > 1) {
            var prevParams = new URLSearchParams(params);
            prevParams.set('page', data.page - 1);
            nav += '<a href="/?' + prevParams.toString() + '" class="pagination-link pagination-prev">← Prev</a>';
        }
        for (var p = 1; p <= data.pages; p++) {
            if (p === data.page) {
                nav += '<span class="pagination-link pagination-current">' + p + '</span>';
            } else if (p <= 3 || p > data.pages - 2 || (p >= data.page - 1 && p <= data.page + 1)) {
                var pageParams = new URLSearchParams(params);
                pageParams.set('page', p);
                nav += '<a href="/?' + pageParams.toString() + '" class="pagination-link">' + p + '</a>';
            } else if (p === 4 || p === data.pages - 2) {
                nav += '<span class="pagination-link pagination-ellipsis">…</span>';
            }
        }
        if (data.page < data.pages) {
            var nextParams = new URLSearchParams(params);
            nextParams.set('page', data.page + 1);
            nav += '<a href="/?' + nextParams.toString() + '" class="pagination-link pagination-next">Next →</a>';
        }
        nav += '</nav>';
        return nav;
    }

    function escapeHtml(str) {
        if (!str) return '';
        var div = document.createElement('div');
        div.appendChild(document.createTextNode(str));
        return div.innerHTML;
    }

    function capitalize(str) {
        if (!str) return '';
        return str.charAt(0).toUpperCase() + str.slice(1);
    }

    function fmtNum(n) {
        return n.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ',');
    }
})();
