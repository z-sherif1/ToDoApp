/* ==========================================================================
   TaskFlow – main.js
   Theme switching, sidebar behavior, password show/hide.

   State lives on <html>:
     data-theme="light|dark"      -> theme       (localStorage: taskflow-theme)
     .sidebar-collapsed           -> desktop     (localStorage: taskflow-sidebar)
     .sidebar-open                -> mobile only (never persisted)

   The inline <head> script in base.html applies the saved state before first
   paint. This file keeps that state in sync and handles user interaction.
   ========================================================================== */

(function () {
    "use strict";

    var root = document.documentElement;

    var THEME_KEY = "taskflow-theme";
    var SIDEBAR_KEY = "taskflow-sidebar";
    var mobileQuery = window.matchMedia("(max-width: 768px)");

    /* ---------- Helpers ---------- */

    function storageSet(key, value) {
        try {
            localStorage.setItem(key, value);
        } catch (error) {
            /* Storage unavailable: the app still works, just without persistence. */
        }
    }

    function storageRemove(key) {
        try {
            localStorage.removeItem(key);
        } catch (error) {
            /* Ignore. */
        }
    }

    function isMobile() {
        return mobileQuery.matches;
    }

    function onMediaChange(query, handler) {
        if (typeof query.addEventListener === "function") {
            query.addEventListener("change", handler);
        } else if (typeof query.addListener === "function") {
            query.addListener(handler); /* Older Safari */
        }
    }


    /* ---------- Theme ---------- */

    function initTheme() {
        var toggle = document.getElementById("themeToggle");

        function currentTheme() {
            return root.getAttribute("data-theme") === "dark" ? "dark" : "light";
        }

        function applyTheme(theme) {
            var isDark = theme === "dark";
            var label = isDark ? "Switch to light mode" : "Switch to dark mode";

            root.setAttribute("data-theme", isDark ? "dark" : "light");
            root.setAttribute("data-bs-theme", isDark ? "dark" : "light");

            if (toggle) {
                toggle.setAttribute("aria-label", label);
                toggle.setAttribute("title", label);
            }
        }

        /* Sync the button labels with the theme already set by base.html. */
        applyTheme(currentTheme());

        if (toggle) {
            toggle.addEventListener("click", function () {
                var nextTheme = currentTheme() === "dark" ? "light" : "dark";

                applyTheme(nextTheme);
                storageSet(THEME_KEY, nextTheme);
            });
        }
    }


    /* ---------- Sidebar ---------- */

    function initSidebar() {
        var sidebar = document.getElementById("sidebar");
        var toggle = document.getElementById("sidebarToggle");
        var overlay = document.getElementById("sidebarOverlay");

        if (!sidebar || !toggle) {
            return;
        }

        function isMobileOpen() {
            return root.classList.contains("sidebar-open");
        }

        function syncAria() {
            var expanded = isMobile()
                ? isMobileOpen()
                : !root.classList.contains("sidebar-collapsed");

            toggle.setAttribute("aria-expanded", expanded ? "true" : "false");
        }

        function openMobileSidebar() {
            root.classList.add("sidebar-open");
            syncAria();
        }

        function closeMobileSidebar(returnFocus) {
            if (!isMobileOpen()) {
                return;
            }

            root.classList.remove("sidebar-open");
            syncAria();

            if (returnFocus) {
                toggle.focus();
            }
        }

        function toggleDesktopSidebar() {
            var collapsed = root.classList.toggle("sidebar-collapsed");

            if (collapsed) {
                storageSet(SIDEBAR_KEY, "collapsed");
            } else {
                storageRemove(SIDEBAR_KEY);
            }

            syncAria();
        }

        /* Toggle button */
        toggle.addEventListener("click", function () {
            if (isMobile()) {
                if (isMobileOpen()) {
                    closeMobileSidebar(false);
                } else {
                    openMobileSidebar();
                }
            } else {
                toggleDesktopSidebar();
            }
        });

        /* Click outside (overlay) closes the mobile sidebar */
        if (overlay) {
            overlay.addEventListener("click", function () {
                closeMobileSidebar(false);
            });
        }

        /* Selecting a navigation link closes the mobile sidebar */
        sidebar.addEventListener("click", function (event) {
            var link = event.target.closest("a");

            if (link && isMobile()) {
                closeMobileSidebar(false);
            }
        });

        /* Escape closes the mobile sidebar */
        document.addEventListener("keydown", function (event) {
            if (event.key === "Escape") {
                closeMobileSidebar(true);
            }
        });

        /* Crossing the breakpoint: never leave the mobile state behind */
        onMediaChange(mobileQuery, function () {
            root.classList.remove("sidebar-open");
            syncAria();
        });

        syncAria();
    }


    /* ---------- Password show / hide ---------- */

    function bindPasswordToggle(input, button) {
        if (button.getAttribute("data-bound") === "true") {
            return;
        }

        button.setAttribute("data-bound", "true");

        var icon = button.querySelector("i");

        if (!icon) {
            icon = document.createElement("i");
            button.appendChild(icon);
        }

        function render(isVisible) {
            icon.className = isVisible ? "bi bi-eye-slash" : "bi bi-eye";
            button.setAttribute("aria-label", isVisible ? "Hide password" : "Show password");
        }

        render(input.type === "text");

        button.addEventListener("click", function () {
            var showPassword = input.type === "password";

            input.type = showPassword ? "text" : "password";
            render(showPassword);
        });
    }

    function initPasswordToggles() {
        /* 1. Templates that already contain the wrapper and button */
        document.querySelectorAll(".password-wrapper").forEach(function (wrapper) {
            var input = wrapper.querySelector("input");
            var button = wrapper.querySelector(".password-toggle");

            if (input && button) {
                bindPasswordToggle(input, button);
            }
        });

        /* 2. Bare password inputs (for example, rendered by a Django form) */
        document.querySelectorAll('input[type="password"]').forEach(function (input) {
            if (input.closest(".password-wrapper")) {
                return;
            }

            var wrapper = document.createElement("div");
            wrapper.className = "password-wrapper";

            input.parentNode.insertBefore(wrapper, input);
            wrapper.appendChild(input);

            var button = document.createElement("button");
            button.type = "button";
            button.className = "password-toggle";
            wrapper.appendChild(button);

            bindPasswordToggle(input, button);
        });
    }


    /* ---------- Start ---------- */

    function init() {
        initTheme();
        initSidebar();
        initPasswordToggles();
    }

    if (document.readyState === "loading") {
        document.addEventListener("DOMContentLoaded", init);
    } else {
        init();
    }
})();