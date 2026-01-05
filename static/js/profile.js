document.addEventListener("DOMContentLoaded", () => {
    // --- AUTH CHECK ---
    const isLoggedIn = localStorage.getItem("isLoggedIn") === "true";
    if (!isLoggedIn) {
        window.location.href = "/login";
        return;
    }

    // --- DATA ---
    let userData = JSON.parse(localStorage.getItem("userProfile")) || {
        name: "John",
        lastname: "Doe",
        email: "john.doe@example.com",
        phone: "+52 55 1234 5678",
        address: "Av. Reforma 222, CDMX",
        avatar: "https://images.unsplash.com/photo-1472099645785-5658abf4ff4e?auto=format&fit=crop&q=80&w=300",
    };

    let orders = JSON.parse(localStorage.getItem("orders")) || [
        {
            id: "#ORD-9821",
            date: "22 Oct 2023",
            total: 45.0,
            status: "completed",
            items: ["Xiaomi Mi Account Unlock"],
            reviewed: false,
        },
        {
            id: "#ORD-9822",
            date: "25 Oct 2023",
            total: 199.99,
            status: "processing",
            items: ["Wireless Headphones"],
            reviewed: false,
        },
    ];

    // --- DOM ELEMENTS ---
    const profileForm = document.getElementById("profile-form");
    const ordersList = document.getElementById("orders-list");
    const noOrders = document.getElementById("no-orders");
    const reviewModal = document.getElementById("review-modal");
    const reviewModalBg = document.getElementById("review-modal-bg");
    const reviewModalContent = document.getElementById("review-modal-content");
    const themeToggle = document.getElementById("setting-theme-toggle");
    const themeIcon = document.getElementById("setting-theme-icon");
    const themeIconBg = document.getElementById("setting-theme-icon-bg");

    let currentReviewId = null;
    let currentRating = 5;

    // --- INIT VIEWS ---
    renderProfile();
    renderOrders();
    initThemeToggle();

    // --- FUNCTION: RENDER PROFILE ---
    function renderProfile() {
        document.getElementById(
            "display-name"
        ).textContent = `${userData.name} ${userData.lastname}`;
        document.getElementById("display-email").textContent = userData.email;
        document.getElementById("user-avatar").src = userData.avatar;

        document.getElementById("input-name").value = userData.name;
        document.getElementById("input-lastname").value = userData.lastname;
        document.getElementById("input-phone").value = userData.phone;
        document.getElementById("input-email").value = userData.email;
        document.getElementById("input-address").value = userData.address;
    }

    // --- FUNCTION: RENDER ORDERS ---
    function renderOrders() {
        ordersList.innerHTML = "";

        if (orders.length === 0) {
            noOrders.classList.remove("hidden");
            return;
        }
        noOrders.classList.add("hidden");

        orders.forEach((order) => {
            let statusBadge = "";
            let statusLabel = "";

            switch (order.status) {
                case "completed":
                    statusBadge =
                        "bg-green-100 text-green-700 dark:bg-green-900/30 dark:text-green-400";
                    statusLabel = "Completado";
                    break;
                case "processing":
                    statusBadge =
                        "bg-blue-100 text-blue-700 dark:bg-blue-900/30 dark:text-blue-400";
                    statusLabel = "Procesando";
                    break;
                default:
                    statusBadge =
                        "bg-orange-100 text-orange-700 dark:bg-orange-900/30 dark:text-orange-400";
                    statusLabel = "Pendiente";
            }

            const itemsStr = order.items.join(", ");
            const extraItems =
                order.items.length > 1 ? ` +${order.items.length - 1} más` : "";

            const html = `
                <div class="bg-white dark:bg-card-dark rounded-3xl shadow-sm border border-gray-100 dark:border-gray-800 p-6 flex flex-col md:flex-row gap-6 items-start md:items-center transition-all hover:shadow-md">
                    <div class="flex-1">
                        <div class="flex items-center gap-3 mb-2">
                            <span class="font-bold text-lg text-primary dark:text-white">${
                                order.id
                            }</span>
                            <span class="px-3 py-1 rounded-full text-xs font-bold uppercase ${statusBadge}">
                                ${statusLabel}
                            </span>
                        </div>
                        <p class="text-sm text-gray-500 mb-1">Fecha: ${
                            order.date
                        }</p>
                        <p class="text-sm font-medium text-gray-700 dark:text-gray-300 truncate max-w-md">
                            ${order.items[0]}${extraItems}
                        </p>
                    </div>
                    
                    <div class="text-right flex flex-col items-end gap-2 w-full md:w-auto">
                        <span class="text-xl font-bold text-primary dark:text-white">$${order.total.toFixed(
                            2
                        )}</span>
                        
                        ${
                            order.status === "completed" && !order.reviewed
                                ? `
                            <button onclick="openReview('${order.id}')" class="px-4 py-2 bg-yellow-400 hover:bg-yellow-500 text-black font-bold rounded-xl text-sm transition-colors flex items-center gap-2 shadow-sm">
                                <span class="material-icons text-sm">star</span> Calificar
                            </button>
                        `
                                : ""
                        }
                        
                        ${
                            order.reviewed
                                ? `
                            <span class="flex items-center gap-1 text-xs font-bold text-green-500 bg-green-50 dark:bg-green-900/10 px-3 py-1.5 rounded-lg">
                                <span class="material-icons text-xs">check_circle</span> Reseña enviada
                            </span>
                        `
                                : ""
                        }

                        ${
                            order.status === "pending" ||
                            order.status === "processing"
                                ? `
                            <button class="text-sm text-accent font-medium hover:underline">Ver Estado</button>
                        `
                                : ""
                        }
                    </div>
                </div>
                `;
            ordersList.insertAdjacentHTML("beforeend", html);
        });
    }

    // --- SAVE PROFILE ---
    profileForm.addEventListener("submit", (e) => {
        e.preventDefault();
        userData.name = document.getElementById("input-name").value;
        userData.lastname = document.getElementById("input-lastname").value;
        userData.phone = document.getElementById("input-phone").value;
        userData.address = document.getElementById("input-address").value;

        localStorage.setItem("userProfile", JSON.stringify(userData));
        renderProfile();
        showToast("Perfil actualizado correctamente");
    });

    // --- LOGOUT ---
    document.getElementById("btn-logout").addEventListener("click", () => {
        if (confirm("¿Cerrar sesión?")) {
            localStorage.removeItem("isLoggedIn");
            window.location.href = "/login"; // Or landing
        }
    });

    // --- TABS LOGIC ---
    window.switchTab = (tabName) => {
        // Hide all
        document
            .querySelectorAll(".tab-content")
            .forEach((el) => el.classList.add("hidden"));

        // Reset Nav Buttons
        document.querySelectorAll(".nav-btn").forEach((btn) => {
            btn.classList.remove(
                "border-accent",
                "bg-gray-50",
                "dark:bg-gray-800",
                "text-accent",
                "font-bold"
            );
            btn.classList.add(
                "border-transparent",
                "text-gray-600",
                "dark:text-gray-400",
                "hover:bg-gray-50",
                "dark:hover:bg-gray-800"
            );
        });

        // Show Active
        document.getElementById(`tab-${tabName}`).classList.remove("hidden");
        const activeBtn = document.getElementById(`nav-${tabName}`);
        activeBtn.classList.remove(
            "border-transparent",
            "text-gray-600",
            "dark:text-gray-400",
            "hover:bg-gray-50",
            "dark:hover:bg-gray-800"
        );
        activeBtn.classList.add(
            "border-accent",
            "bg-gray-50",
            "dark:bg-gray-800",
            "text-accent",
            "font-bold"
        );
    };

    // --- REVIEW MODAL LOGIC ---
    window.openReview = (id) => {
        currentReviewId = id;
        currentRating = 5;
        document.getElementById("review-order-id").textContent = `Pedido ${id}`;
        document.getElementById("review-text").value = "";
        renderStars();

        reviewModal.classList.remove("hidden");
        setTimeout(() => {
            reviewModalBg.classList.remove("opacity-0");
            reviewModalContent.classList.remove("opacity-0", "translate-y-10");
        }, 10);
    };

    function closeReview() {
        reviewModalBg.classList.add("opacity-0");
        reviewModalContent.classList.add("opacity-0", "translate-y-10");
        setTimeout(() => {
            reviewModal.classList.add("hidden");
            currentReviewId = null;
        }, 300);
    }

    document
        .getElementById("btn-cancel-review")
        .addEventListener("click", closeReview);
    reviewModalBg.addEventListener("click", closeReview);

    function renderStars() {
        const container = document.getElementById("star-container");
        container.innerHTML = "";
        for (let i = 1; i <= 5; i++) {
            const isActive = i <= currentRating;
            const star = document.createElement("button");
            star.className = `transition-transform hover:scale-110 ${
                isActive
                    ? "text-yellow-400"
                    : "text-gray-300 dark:text-gray-700"
            }`;
            star.innerHTML =
                '<span class="material-icons text-4xl">star</span>';
            star.onclick = () => {
                currentRating = i;
                renderStars();
            };
            container.appendChild(star);
        }
    }

    document
        .getElementById("btn-submit-review")
        .addEventListener("click", () => {
            if (!currentReviewId) return;

            // Update Order
            orders = orders.map((o) =>
                o.id === currentReviewId ? { ...o, reviewed: true } : o
            );
            localStorage.setItem("orders", JSON.stringify(orders));

            renderOrders();
            closeReview();
            showToast("¡Gracias por tu reseña!");
        });

    // --- THEME SETTINGS ---
    function initThemeToggle() {
        const isDark = document.documentElement.classList.contains("dark");
        themeToggle.checked = isDark;
        updateThemeUI(isDark);

        themeToggle.addEventListener("change", () => {
            const html = document.documentElement;
            if (themeToggle.checked) {
                html.classList.add("dark");
                localStorage.setItem("theme", "dark");
                updateThemeUI(true);
            } else {
                html.classList.remove("dark");
                localStorage.setItem("theme", "light");
                updateThemeUI(false);
            }

            // Force sync with Navbar toggle if present (optional)
            const navToggleIcon = document.getElementById("theme-icon");
            if (navToggleIcon)
                navToggleIcon.textContent = themeToggle.checked
                    ? "dark_mode"
                    : "light_mode";
        });
    }

    function updateThemeUI(isDark) {
        if (isDark) {
            themeIcon.textContent = "dark_mode";
            themeIconBg.classList.remove("bg-yellow-400");
            themeIconBg.classList.add("bg-indigo-500");
        } else {
            themeIcon.textContent = "light_mode";
            themeIconBg.classList.remove("bg-indigo-500");
            themeIconBg.classList.add("bg-yellow-400");
        }
    }

    function showToast(msg) {
        const toast = document.getElementById("profile-toast");
        const toastMsg = document.getElementById("toast-msg");
        toastMsg.textContent = msg;

        toast.classList.remove("translate-x-10", "opacity-0");
        toast.classList.add("translate-x-0", "opacity-100");

        setTimeout(() => {
            toast.classList.remove("translate-x-0", "opacity-100");
            toast.classList.add("translate-x-10", "opacity-0");
        }, 3000);
    }
});
