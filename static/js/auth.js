document.addEventListener("DOMContentLoaded", () => {
    let isRegister = false;

    // Elements
    const authTitle = document.getElementById("auth-title");
    const authSubtitle = document.getElementById("auth-subtitle");
    const nameContainer = document.getElementById("name-container");
    const submitText = document.getElementById("submit-text");
    const toggleBtn = document.getElementById("toggle-btn");
    const toggleQuestion = document.getElementById("toggle-question");
    const forgotLink = document.getElementById("forgot-link");
    const authForm = document.getElementById("auth-form");
    const errorMsg = document.getElementById("error-message");
    const errorText = document.getElementById("error-text");
    const inputs = document.querySelectorAll(".error-target");

    // Toggle Logic
    toggleBtn.addEventListener("click", (e) => {
        e.preventDefault();
        isRegister = !isRegister;
        updateView();
        clearErrors();
    });

    function updateView() {
        if (isRegister) {
            authTitle.textContent = "Únete a la Comunidad";
            authSubtitle.textContent = "Crea tu cuenta en segundos";
            nameContainer.classList.remove("hidden");
            nameContainer.classList.add("block", "animate-slide-up"); // Visual animation
            submitText.textContent = "Crear Cuenta";
            toggleQuestion.textContent = "¿Ya tienes cuenta?";
            toggleBtn.textContent = "Inicia Sesión";
            forgotLink.classList.add("hidden"); // Hide forgot link in register
        } else {
            authTitle.textContent = "¡Hola de nuevo!";
            authSubtitle.textContent =
                "Ingresa tus credenciales para continuar";
            nameContainer.classList.add("hidden");
            nameContainer.classList.remove("block", "animate-slide-up");
            submitText.textContent = "Iniciar Sesión";
            toggleQuestion.textContent = "¿No tienes cuenta?";
            toggleBtn.textContent = "Regístrate Gratis";
            forgotLink.classList.remove("hidden");
        }
    }

    function clearErrors() {
        errorMsg.classList.add("hidden");
        errorMsg.classList.remove("flex");
        inputs.forEach((input) => {
            input.classList.remove(
                "border-red-500",
                "bg-red-50",
                "dark:bg-red-900/10"
            );
        });
    }

    function showError(msg) {
        errorText.textContent = msg;
        errorMsg.classList.remove("hidden");
        errorMsg.classList.add("flex");
        inputs.forEach((input) => {
            input.classList.add(
                "border-red-500",
                "bg-red-50",
                "dark:bg-red-900/10"
            );
        });
    }

    // Form Submit Logic
    authForm.addEventListener("submit", (e) => {
        e.preventDefault();
        const email = document.getElementById("email").value;
        const password = document.getElementById("password").value;
        const name = document.getElementById("name").value;

        // Simple Mock Validation
        if (isRegister) {
            if (!name || !email || !password) {
                showError("Por favor completa todos los campos.");
                return;
            }
            showToast(`Bienvenido a la familia Xiaomi, ${name}!`);
            setTimeout(() => {
                window.location.href = "/"; // Redirect to home
            }, 1500);
        } else {
            if (email === "admin" && password === "12345") {
                showToast("Sesión iniciada correctamente");
                localStorage.setItem("isLoggedIn", "true"); // Simulate session
                setTimeout(() => {
                    window.location.href = "/"; // Redirect to home
                }, 1000);
            } else {
                showError("Credenciales incorrectas. Intenta: admin / 12345");
            }
        }
    });

    // Toast Logic
    function showToast(message) {
        const container = document.getElementById("toast-container");
        const msgEl = document.getElementById("toast-message");

        msgEl.textContent = message;
        container.classList.remove("translate-x-10", "opacity-0");
        container.classList.add("translate-x-0", "opacity-100");

        setTimeout(() => {
            container.classList.remove("translate-x-0", "opacity-100");
            container.classList.add("translate-x-10", "opacity-0");
        }, 3000);
    }

    // Clear errors on input logic
    inputs.forEach((input) => {
        input.addEventListener("input", clearErrors);
    });
});
