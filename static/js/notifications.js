/* ==========================================================================
   TaskFlow – notifications.js
   Closes Django messages: manual close button + automatic dismissal.

   Markup (from base.html):
     .django-messages
       .django-message.{success|error|warning|info}
         .message-icon, .message-text, button.notification-close

   CSS (from base.css): .notification-hidden fades the message out.
   ========================================================================== */

(function () {
    "use strict";

    var AUTO_CLOSE_DELAY = 5000;        /* success / info  */
    var AUTO_CLOSE_DELAY_LONG = 10000;  /* error / warning */
    var FALLBACK_REMOVE_DELAY = 400;    /* safety net if transitionend never fires */

    var reduceMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

    function removeEmptyContainer(container) {
        if (container && !container.querySelector(".django-message")) {
            container.remove();
        }
    }

    function setupNotification(notification) {
        var container = notification.parentElement;
        var closeButton = notification.querySelector(".notification-close");
        var isImportant =
            notification.classList.contains("error") ||
            notification.classList.contains("warning");
        var delay = isImportant ? AUTO_CLOSE_DELAY_LONG : AUTO_CLOSE_DELAY;
        var timerId = null;
        var isClosing = false;

        if (notification.classList.contains("error")) {
            notification.setAttribute("role", "alert");
        }

        function finishRemoval() {
            notification.remove();
            removeEmptyContainer(container);
        }

        function closeNotification() {
            if (isClosing) {
                return;
            }

            isClosing = true;
            window.clearTimeout(timerId);

            if (reduceMotion) {
                finishRemoval();
                return;
            }

            notification.classList.add("notification-hidden");

            var removed = false;

            function removeOnce() {
                if (removed) {
                    return;
                }
                removed = true;
                finishRemoval();
            }

            notification.addEventListener("transitionend", removeOnce, { once: true });
            window.setTimeout(removeOnce, FALLBACK_REMOVE_DELAY);
        }

        function startTimer() {
            window.clearTimeout(timerId);
            timerId = window.setTimeout(closeNotification, delay);
        }

        function pauseTimer() {
            window.clearTimeout(timerId);
        }

        if (closeButton) {
            closeButton.addEventListener("click", closeNotification);
        }

        /* Pause while the user is reading or interacting with the message */
        notification.addEventListener("mouseenter", pauseTimer);
        notification.addEventListener("mouseleave", function () {
            if (!isClosing) {
                startTimer();
            }
        });
        notification.addEventListener("focusin", pauseTimer);
        notification.addEventListener("focusout", function () {
            if (!isClosing) {
                startTimer();
            }
        });

        startTimer();
    }

    function init() {
        document.querySelectorAll(".django-message").forEach(setupNotification);
    }

    if (document.readyState === "loading") {
        document.addEventListener("DOMContentLoaded", init);
    } else {
        init();
    }
})();