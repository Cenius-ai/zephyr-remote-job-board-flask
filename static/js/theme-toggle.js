/* ================================================================
   Zephyr — Light/Dark Theme Toggle
   Persists preference via localStorage; syncs both toggle buttons.
   ================================================================ */

(function () {
    'use strict';

    var KEY = 'zephyr-theme';

    function getStoredTheme() {
        try {
            return localStorage.getItem(KEY);
        } catch (_) {
            return null;
        }
    }

    function setStoredTheme(theme) {
        try {
            localStorage.setItem(KEY, theme);
        } catch (_) {}
    }

    function applyTheme(theme) {
        document.documentElement.setAttribute('data-theme', theme);
    }

    function toggleTheme() {
        var current = document.documentElement.getAttribute('data-theme');
        var next = current === 'dark' ? 'light' : 'dark';
        applyTheme(next);
        setStoredTheme(next);
    }

    // Initialize on load
    var stored = getStoredTheme();
    if (stored) {
        applyTheme(stored);
    } else {
        // Check OS preference
        if (window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches) {
            applyTheme('dark');
        }
    }

    // Desktop toggle
    var toggleBtn = document.getElementById('theme-toggle');
    if (toggleBtn) {
        toggleBtn.addEventListener('click', toggleTheme);
    }

    // Mobile toggle
    var toggleMobile = document.getElementById('theme-toggle-mobile');
    if (toggleMobile) {
        toggleMobile.addEventListener('click', toggleTheme);
    }

    // Listen for OS changes
    if (window.matchMedia) {
        window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', function (e) {
            if (!getStoredTheme()) {
                applyTheme(e.matches ? 'dark' : 'light');
            }
        });
    }
})();
