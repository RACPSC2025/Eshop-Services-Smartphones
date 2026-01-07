document.addEventListener("DOMContentLoaded", () => {
    const themeToggle = document.getElementById("theme-toggle");
    const themeIcon = document.getElementById("theme-icon");
    const html = document.documentElement;

    // Set initial icon based on the class set by theme.js
    if (themeIcon) {
        themeIcon.textContent = html.classList.contains("dark") ? "dark_mode" : "light_mode";
    }

    // Event Listener
    if (themeToggle) {
        themeToggle.addEventListener("click", () => {
            html.classList.toggle("dark");
            const isDark = html.classList.contains("dark");
            localStorage.setItem("theme", isDark ? "dark" : "light");
            if (themeIcon)
                themeIcon.textContent = isDark ? "dark_mode" : "light_mode";
        });
    }
});
