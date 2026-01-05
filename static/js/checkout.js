document.addEventListener("DOMContentLoaded", () => {
    // --- DATA ---
    let cartItems = JSON.parse(localStorage.getItem("cartItems")) || [];

    // Redirect if empty
    if (cartItems.length === 0) {
        window.location.href = "/cart";
        return;
    }

    // --- RENDER SIDEBAR ---
    const itemsContainer = document.getElementById("checkout-items");
    let subtotal = 0;

    cartItems.forEach((item) => {
        subtotal += item.price * item.qty;
        const html = `
            <div class="flex items-start space-x-4 group">
                <div class="flex-shrink-0 w-20 h-20 bg-gray-50 dark:bg-gray-700 rounded-xl border border-gray-100 dark:border-gray-600 p-2 relative">
                    <img src="${item.image}" alt="${
            item.name
        }" class="w-full h-full object-contain mix-blend-multiply dark:mix-blend-normal"/>
                    <span class="absolute -top-2 -right-2 bg-primary text-white text-xs font-bold w-6 h-6 flex items-center justify-center rounded-full shadow-md border-2 border-white dark:border-card-dark">${
                        item.qty
                    }</span>
                </div>
                <div class="flex-1">
                    <p class="text-sm font-bold text-primary dark:text-white line-clamp-2">${
                        item.name
                    }</p>
                    <p class="text-xs text-gray-500 mt-1">${
                        item.category === "products"
                            ? "Producto Físico"
                            : "Servicio Digital"
                    }</p>
                </div>
                <div class="text-sm font-bold text-primary dark:text-white">$${(
                    item.price * item.qty
                ).toFixed(2)}</div>
            </div>
            `;
        itemsContainer.insertAdjacentHTML("beforeend", html);
    });

    // Calculations
    const serviceFee = cartItems.length > 0 ? 15.0 : 0;
    const tax = subtotal * 0.085;
    const total = subtotal + serviceFee + tax;

    // Update Text
    document.getElementById(
        "checkout-subtotal"
    ).textContent = `$${subtotal.toFixed(2)}`;
    document.getElementById(
        "checkout-fee"
    ).textContent = `$${serviceFee.toFixed(2)}`;
    document.getElementById("checkout-tax").textContent = `$${tax.toFixed(2)}`;
    document.getElementById("checkout-total").textContent = `$${total.toFixed(
        2
    )}`;
    document.getElementById("btn-pay-amount").textContent = total.toFixed(2);

    // --- PAYMENT METHOD TOGGLE ---
    const opts = document.querySelectorAll(".payment-option");
    const stripeForm = document.getElementById("stripe-form");
    const paypalInfo = document.getElementById("paypal-info");
    const btnText = document.getElementById("btn-pay-text");

    opts.forEach((opt) => {
        opt.addEventListener("click", () => {
            const method = opt.dataset.method;

            // Update Radio
            document.querySelector(
                `input[name="payment_method"][value="${method}"]`
            ).checked = true;

            // Update UI Styles
            opts.forEach((o) => {
                o.classList.remove("bg-gray-50", "dark:bg-gray-800/80");
                o.classList.add("bg-white", "dark:bg-card-dark");
            });
            opt.classList.remove("bg-white", "dark:bg-card-dark");
            opt.classList.add("bg-gray-50", "dark:bg-gray-800/80");

            // Show/Hide Sections
            if (method === "stripe") {
                stripeForm.classList.remove("hidden");
                paypalInfo.classList.add("hidden");
                btnText.innerHTML = `Pagar $<span id="btn-pay-amount">${total.toFixed(
                    2
                )}</span> <span class="material-icons ml-2">arrow_forward</span>`;
            } else {
                stripeForm.classList.add("hidden");
                paypalInfo.classList.remove("hidden");
                btnText.innerHTML = `Continuar con PayPal <span class="material-icons ml-2">arrow_forward</span>`;
            }
        });
    });

    // --- SUBMIT LOGIC ---
    const form = document.getElementById("checkout-form");
    const btnPay = document.getElementById("btn-pay");
    const btnLoader = document.getElementById("btn-pay-loader");

    form.addEventListener("submit", (e) => {
        e.preventDefault();

        // UI Loading
        btnPay.disabled = true;
        btnText.classList.add("hidden");
        btnLoader.classList.remove("hidden");
        btnPay.classList.add("opacity-75", "cursor-not-allowed");

        // Simulate API Call
        setTimeout(() => {
            // Success
            const newOrder = {
                id: `#ORD-${Math.floor(1000 + Math.random() * 9000)}`,
                date: new Date().toLocaleDateString("es-ES", {
                    day: "2-digit",
                    month: "short",
                    year: "numeric",
                }),
                total: total,
                status: "processing",
                items: cartItems.map((i) => i.name),
                reviewed: false,
            };

            // Get existing orders from localStorage
            let orders = JSON.parse(localStorage.getItem("orders")) || [];
            orders.unshift(newOrder);
            localStorage.setItem("orders", JSON.stringify(orders));

            // Clear Cart
            localStorage.setItem("cartItems", JSON.stringify([]));

            // Redirect to Profile (Orders Tab)
            // In a real Django app: window.location.href = '{% url "profile" %}?tab=orders';
            window.location.href = "/profile"; // Assuming we'll build this route next
        }, 2500);
    });
});
