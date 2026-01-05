document.addEventListener("DOMContentLoaded", () => {
    const form = document.getElementById("contact-form");
    const toast = document.getElementById("contact-toast");

    form.addEventListener("submit", (e) => {
        e.preventDefault();

        // Simular envío
        const btn = form.querySelector('button[type="submit"]');
        const originalContent = btn.innerHTML;

        // Loading State
        btn.disabled = true;
        btn.innerHTML =
            '<span class="w-5 h-5 border-2 border-white/30 border-t-white rounded-full animate-spin"></span>';

        setTimeout(() => {
            // Success State
            btn.disabled = false;
            btn.innerHTML = originalContent;
            form.reset();
            showToast();
        }, 1500);
    });

    function showToast() {
        toast.classList.remove("translate-x-10", "opacity-0");
        toast.classList.add("translate-x-0", "opacity-100");

        setTimeout(() => {
            toast.classList.remove("translate-x-0", "opacity-100");
            toast.classList.add("translate-x-10", "opacity-0");
        }, 4000);
    }
});
