// Usamos un bloque para evitar errores si el elemento no existe en alguna página
document.addEventListener("DOMContentLoaded", () => {
    const themeToggle = document.getElementById("theme-toggle");
    const themeIcon = document.getElementById("theme-icon");
    const html = document.documentElement;

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
