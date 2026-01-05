document.addEventListener("DOMContentLoaded", () => {
    const themeToggle = document.getElementById("theme-toggle");
    const themeIcon = document.getElementById("theme-icon");
    const html = document.documentElement;

    // 1. Check LocalStorage on load
    const savedTheme = localStorage.getItem("theme");
    if (savedTheme === 'dark' || (!savedTheme && window.matchMedia('(prefers-color-scheme: dark)').matches)) {
        html.classList.add('dark');
        if (themeIcon) themeIcon.textContent = "dark_mode";
    } else {
        html.classList.remove('dark');
        if (themeIcon) themeIcon.textContent = "light_mode";
    }

    // 2. Event Listener
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
