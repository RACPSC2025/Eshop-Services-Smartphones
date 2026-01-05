/** @type {import('tailwindcss').Config} */
module.exports = {
    content: [
        "./templates/**/*.html", // Para templates en la raíz
        "./apps/**/templates/**/*.html", // Para templates dentro de apps
        "./core/**/templates/**/*.html", // Para templates en core
        "./**/forms.py", // Para clases en archivos de formularios
    ],

    theme: {
        extend: {},
    },
    plugins: [],
};
