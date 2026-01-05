// --- STATE ---
let currentPrice = 45.0;
let currentLabel = "Servicio Estándar";
let productId = "serv-screen-amoled"; // Mock ID

document.addEventListener("DOMContentLoaded", () => {
    // --- GALLERY LOGIC ---
    const mainImg = document.getElementById("main-image");
    const thumbs = document.querySelectorAll(".thumb-btn");

    thumbs.forEach((btn) => {
        btn.addEventListener("click", function () {
            // Update Main Image
            const src = this.dataset.src;
            mainImg.src = src;

            // Update Active State
            thumbs.forEach((t) => {
                t.classList.remove("border-accent", "ring-2", "ring-accent/20");
                t.classList.add("border-transparent", "opacity-70");
            });
            this.classList.remove("border-transparent", "opacity-70");
            this.classList.add("border-accent", "ring-2", "ring-accent/20");
        });
    });

    // --- STICKY BAR LOGIC ---
    const stickyBar = document.getElementById("sticky-bar");
    const ctaContainer = document.getElementById("main-cta-container");

    window.addEventListener("scroll", () => {
        const rect = ctaContainer.getBoundingClientRect();
        // Show bar when main CTA scrolls out of view (top < -50)
        if (rect.top < -50) {
            stickyBar.classList.remove("translate-y-full");
        } else {
            stickyBar.classList.add("translate-y-full");
        }
    });
});

// --- OPTIONS LOGIC ---
window.selectOption = (el) => {
    // Reset styles for all options
    document.querySelectorAll(".service-option").forEach((opt) => {
        opt.classList.remove("border-accent", "bg-accent/5");
        opt.classList.add("border-gray-100", "dark:border-gray-700");

        // Handle Radio Indicator
        const indicator = opt.querySelector(".radio-indicator");
        indicator.classList.remove("border-accent");
        indicator.classList.add("border-gray-300");
        opt.querySelector(".radio-indicator div").classList.add("hidden");

        // Handle Label Color
        opt.querySelector(".option-label").classList.remove("text-accent");
        opt.querySelector(".option-label").classList.add(
            "text-gray-900",
            "dark:text-white"
        );
    });

    // Apply active styles to clicked
    el.classList.remove("border-gray-100", "dark:border-gray-700");
    el.classList.add("border-accent", "bg-accent/5");

    const indicator = el.querySelector(".radio-indicator");
    indicator.classList.remove("border-gray-300");
    indicator.classList.add("border-accent");
    el.querySelector(".radio-indicator div").classList.remove("hidden");

    el.querySelector(".option-label").classList.remove(
        "text-gray-900",
        "dark:text-white"
    );
    el.querySelector(".option-label").classList.add("text-accent");

    // Update State
    currentPrice = parseFloat(el.dataset.price);
    currentLabel = el.dataset.label;

    // Update UI Text
    document.getElementById(
        "sticky-price"
    ).textContent = `$${currentPrice.toFixed(2)}`;
    document.getElementById("sticky-variant").textContent = currentLabel;
};

// --- CART LOGIC ---
window.addToCart = () => {
    const item = {
        id: `${productId}-${currentLabel.replace(/\s+/g, "-").toLowerCase()}`, // Unique ID per variant
        name: `Display Original AMOLED (${currentLabel})`,
        price: currentPrice,
        image: document.getElementById("main-image").src,
        description: "Panel 120Hz con marco.",
        qty: 1,
        category: "services", // Mock category
    };

    // Get existing cart
    let cart = JSON.parse(localStorage.getItem("cartItems")) || [];

    // Check if exists
    const existingIndex = cart.findIndex((i) => i.id === item.id);
    if (existingIndex > -1) {
        cart[existingIndex].qty += 1;
    } else {
        cart.push(item);
    }

    localStorage.setItem("cartItems", JSON.stringify(cart));

    // Dispatch Event to update Navbar
    window.dispatchEvent(new Event("storage"));

    // Show Toast
    const toast = document.getElementById("cart-toast");
    document.getElementById("toast-product-name").textContent = item.name;

    toast.classList.remove("translate-x-10", "opacity-0");
    toast.classList.add("translate-x-0", "opacity-100");

    setTimeout(() => {
        toast.classList.remove("translate-x-0", "opacity-100");
        toast.classList.add("translate-x-10", "opacity-0");
    }, 3000);
};

window.toggleWishlist = (btn) => {
    const icon = btn.querySelector(".material-icons");
    if (icon.textContent === "favorite_border") {
        icon.textContent = "favorite";
        btn.classList.add("text-red-500", "bg-red-50", "border-red-200");
        btn.classList.remove("text-gray-500", "bg-gray-50", "border-gray-100");
    } else {
        icon.textContent = "favorite_border";
        btn.classList.remove("text-red-500", "bg-red-50", "border-red-200");
        btn.classList.add("text-gray-500", "bg-gray-50", "border-gray-100");
    }
};
