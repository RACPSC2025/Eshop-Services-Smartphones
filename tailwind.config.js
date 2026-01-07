/** @type {import('tailwindcss').Config} */
module.exports = {
    darkMode: "class",
    content: [
        "./templates/**/*.html",
        "./static/js/**/*.js",
        "./apps/**/forms.py",
    ],
    theme: {
        extend: {
            colors: {
                "background-dark": "#121212",
                "card-dark": "#1E1E1E",
                "border-dark": "#2C2C2C",
                "text-dark": "#E0E0E0",
                "text-muted-dark": "#A0A0A0",

                "xiaomi": "#FF6900",
                "accent": "#00BCD4",
            },
        },
    },
    plugins: [],
};
