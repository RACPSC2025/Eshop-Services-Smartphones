document.addEventListener("DOMContentLoaded", () => {
    // --- DATA ---
    let cartItems = JSON.parse(localStorage.getItem("cartItems")) || [];
    const isLoggedIn = localStorage.getItem("isLoggedIn") === "true";

    // --- DOM ELEMENTS ---
    const emptyView = document.getElementById("empty-cart-view");
    const cartContent = document.getElementById("cart-content");
    const itemsContainer = document.getElementById("cart-items-container");
    const itemsCountHeader = document.getElementById("items-count-header");

    // Summary Elements
    const elSubtotal = document.getElementById("summary-subtotal");
    const elFee = document.getElementById("summary-fee");
    const elTax = document.getElementById("summary-tax");
    const elTotal = document.getElementById("summary-total");

    // Modal Elements
    const loginModal = document.getElementById("login-modal");
    const modalBg = document.getElementById("login-modal-bg");
    const modalContent = document.getElementById("login-modal-content");
    const btnCheckout = document.getElementById("btn-checkout");
    const btnCloseModal = document.getElementById("btn-close-modal");
    const btnClearCart = document.getElementById("btn-clear-cart");

    // --- FUNCTIONS ---

    function renderCart() {
        if (cartItems.length === 0) {
            emptyView.classList.remove("hidden");
            cartContent.classList.add("hidden");
            return;
        }

        emptyView.classList.add("hidden");
        cartContent.classList.remove("hidden");
        itemsCountHeader.textContent = `${cartItems.length} items agregados`;

        itemsContainer.innerHTML = "";

        cartItems.forEach((item) => {
            const itemTotal = item.price * item.qty;
            const html = `
                <div class="group bg-white dark:bg-card-dark rounded-3xl shadow-sm border border-gray-100 dark:border-gray-700 p-4 sm:p-5 transition-all hover:shadow-xl hover:-translate-y-0.5 relative overflow-hidden">
                    <div class="grid grid-cols-1 sm:grid-cols-12 gap-6 items-center relative z-10">
                        <!-- Product Info -->
                        <div class="col-span-1 sm:col-span-6 flex items-center gap-5">
                            <div class="relative w-24 h-24 flex-shrink-0 bg-gray-50 dark:bg-gray-800 rounded-2xl overflow-hidden border border-gray-200 dark:border-gray-600 group-hover:border-accent/50 transition-colors p-2">
                                <img src="${item.image}" alt="${
                item.name
            }" class="w-full h-full object-contain mix-blend-multiply dark:mix-blend-normal"/>
                            </div>
                            <div>
                                <h3 class="font-bold text-base text-primary dark:text-white leading-tight group-hover:text-accent transition-colors">${
                                    item.name
                                }</h3>
                                <p class="text-xs text-gray-500 dark:text-gray-400 mt-1">${
                                    item.description || ""
                                }</p>
                                <div class="flex items-center gap-3 mt-2">
                                    ${
                                        item.tag
                                            ? `<span class="text-[10px] font-bold text-white ${
                                                  item.tagColor || "bg-gray-500"
                                              } px-2 py-0.5 rounded-full uppercase tracking-wide">${
                                                  item.tag
                                              }</span>`
                                            : ""
                                    }
                                    <button onclick="removeFromCart('${
                                        item.id
                                    }')" class="text-xs text-gray-400 hover:text-red-500 flex items-center gap-1 font-medium transition-colors">
                                        <span class="material-icons text-[14px]">delete</span> Eliminar
                                    </button>
                                </div>
                            </div>
                        </div>
                        <!-- Quantity -->
                        <div class="col-span-1 sm:col-span-2 flex justify-center">
                            <div class="flex items-center border border-gray-200 dark:border-gray-600 rounded-xl overflow-hidden bg-white dark:bg-gray-800 shadow-sm">
                                <button onclick="updateQty('${
                                    item.id
                                }', -1)" class="w-8 h-8 flex items-center justify-center text-gray-500 hover:bg-gray-100 dark:hover:bg-gray-700 transition-colors font-bold">-</button>
                                <span class="w-8 text-center text-sm font-semibold text-primary dark:text-white">${
                                    item.qty
                                }</span>
                                <button onclick="updateQty('${
                                    item.id
                                }', 1)" class="w-8 h-8 flex items-center justify-center text-gray-500 hover:bg-gray-100 dark:hover:bg-gray-700 transition-colors font-bold">+</button>
                            </div>
                        </div>
                        <!-- Price -->
                        <div class="col-span-1 sm:col-span-2 text-left sm:text-right">
                            <span class="sm:hidden text-gray-500 text-sm mr-2">Precio:</span>
                            <span class="text-gray-600 dark:text-gray-300 font-medium text-sm">$${item.price.toFixed(
                                2
                            )}</span>
                        </div>
                        <!-- Total -->
                        <div class="col-span-1 sm:col-span-2 text-left sm:text-right">
                            <span class="sm:hidden text-gray-500 text-sm mr-2">Total:</span>
                            <span class="text-primary dark:text-white font-bold text-base">$${itemTotal.toFixed(
                                2
                            )}</span>
                        </div>
                    </div>
                </div>
                `;
            itemsContainer.insertAdjacentHTML("beforeend", html);
        });

        calculateTotals();
    }

    function calculateTotals() {
        const subtotal = cartItems.reduce(
            (acc, item) => acc + item.price * item.qty,
            0
        );
        const serviceFee = cartItems.length > 0 ? 15.0 : 0;
        const tax = subtotal * 0.085;
        const total = subtotal + serviceFee + tax;

        elSubtotal.textContent = `$${subtotal.toFixed(2)}`;
        elFee.textContent = `$${serviceFee.toFixed(2)}`;
        elTax.textContent = `$${tax.toFixed(2)}`;
        elTotal.textContent = `$${total.toFixed(2)}`;
    }

    function saveCart() {
        localStorage.setItem("cartItems", JSON.stringify(cartItems));
        renderCart();
        // Update Navbar badge if exists (dispatch event)
        window.dispatchEvent(new Event("storage"));
    }

    // --- GLOBAL SCOPE FUNCTIONS (for inline onclicks) ---
    window.updateQty = (id, change) => {
        cartItems = cartItems.map((item) => {
            // Type check because localStorage ids are strings but sometimes comparisons fail
            if (String(item.id) === String(id)) {
                const newQty = Math.max(1, item.qty + change);
                return { ...item, qty: newQty };
            }
            return item;
        });
        saveCart();
    };

    window.removeFromCart = (id) => {
        cartItems = cartItems.filter((item) => String(item.id) !== String(id));
        saveCart();
    };

    // --- EVENT LISTENERS ---

    btnClearCart.addEventListener("click", () => {
        if (confirm("¿Estás seguro de vaciar el carrito?")) {
            cartItems = [];
            saveCart();
        }
    });

    btnCheckout.addEventListener("click", () => {
        if (isLoggedIn) {
            window.location.href = "/checkout";
        } else {
            // Show Modal
            loginModal.classList.remove("hidden");
            // Small delay for animation
            setTimeout(() => {
                modalBg.classList.remove("opacity-0");
                modalContent.classList.remove("translate-y-10", "opacity-0");
            }, 10);
        }
    });

    const closeModal = () => {
        modalBg.classList.add("opacity-0");
        modalContent.classList.add("translate-y-10", "opacity-0");
        setTimeout(() => {
            loginModal.classList.add("hidden");
        }, 300);
    };

    btnCloseModal.addEventListener("click", closeModal);
    modalBg.addEventListener("click", closeModal);

    // --- INIT ---
    renderCart();
});
