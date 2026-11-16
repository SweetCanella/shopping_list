document.addEventListener("DOMContentLoaded", function () {
    var yearElement = document.getElementById("current-year");
    if (yearElement) {
        yearElement.textContent = String(new Date().getFullYear());
    }
});
