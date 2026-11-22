/* ==========================================================================
   TaskFlow – tasks.js
   Delete confirmation for task and category deletion pages.

   A form is treated as a delete confirmation when it is, contains, or sits
   inside an element with the class .confirmation-actions (the layout used by
   the delete confirmation pages). The logout form is not affected.

   Optional: add data-confirm="Custom message" to the form to change the text.
   ========================================================================== */

(function () {
    "use strict";

    var DEFAULT_MESSAGE = "Are you sure you want to delete this item?";

    function isConfirmationForm(form) {
        return (
            form.classList.contains("confirmation-actions") ||
            form.closest(".confirmation-actions") !== null ||
            form.querySelector(".confirmation-actions") !== null
        );
    }

    document.addEventListener("submit", function (event) {
        var form = event.target;

        if (!form || form.tagName !== "FORM" || !isConfirmationForm(form)) {
            return;
        }

        var message = form.getAttribute("data-confirm") || DEFAULT_MESSAGE;

        if (!window.confirm(message)) {
            event.preventDefault();
        }
    });
})();