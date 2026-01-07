/**
 * cart.js for UnlockXiaomi
 * Maneja la lógica asíncrona del carrito de compras.
 */

// Obtener CSRF Token de las cookies
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

// Helper function to get CSRF token
function getCSRFToken() {
    return getCookie('csrftoken');
}

// Helper to check if cart is empty and handle redirects/reloads
function checkEmptyState(count) {
    if (count === 0) {
        console.log('[Cart] Cart is empty. Handling termination...');
        const isCartPage = !!document.getElementById('cart-table-container');
        if (isCartPage) {
            setTimeout(() => location.reload(), 500);
        }
    }
}

/**
 * Agrega un producto al carrito
 * @param {number} productId 
 * @param {number} [quantity=1]
 */
async function addToCart(productId, quantity = 1) {
    console.log(`[Cart] Attempting to add Product ID: ${productId} | Qty: ${quantity}`);
    const csrftoken = getCSRFToken();
    try {
        const response = await fetch(`/orders/api/add/${productId}/`, {
            method: 'POST',
            headers: { 'X-CSRFToken': csrftoken, 'Content-Type': 'application/json' },
            body: JSON.stringify({ quantity })
        });
        const data = await response.json();
        if (data.success) {
            updateCartUI(data);
            showNotification('success', data.message);
        } else if (response.status === 403 && data.error === 'login_required') {
            if (typeof openLoginModal === 'function') openLoginModal();
            else window.location.href = '/users/auth/';
        } else {
            showNotification('error', data.message || 'Error');
        }
    } catch (error) {
        console.error('[Cart] Add error:', error);
    }
}

/**
 * Elimina un item del carrito
 * @param {number} itemId 
 */
async function removeFromCart(itemId) {
    console.log(`[Cart] Removing Item ID: ${itemId}`);
    const csrftoken = getCSRFToken();
    try {
        const response = await fetch(`/orders/api/remove/${itemId}/`, {
            method: 'POST',
            headers: { 'X-CSRFToken': csrftoken }
        });
        const data = await response.json();
        if (data.success) {
            updateCartUI(data);
            if (data.cart_html) updateFullCartTable(data.cart_html);
            checkEmptyState(data.cart_count);
            showNotification('info', data.message);
        }
    } catch (error) {
        console.error('[Cart] Remove error:', error);
    }
}

/**
 * Actualiza la cantidad de un item (+/-)
 * @param {number} itemId 
 * @param {string} action 'increase' or 'decrease'
 */
async function updateCartItem(itemId, action) {
    console.log(`[Cart] Update Action: ${action} | Item: ${itemId}`);
    const csrftoken = getCSRFToken();
    const formData = new FormData();
    formData.append('action', action);

    try {
        const response = await fetch(`/orders/api/update/${itemId}/`, {
            method: 'POST',
            body: formData,
            headers: { 'X-CSRFToken': csrftoken }
        });
        const data = await response.json();
        if (data.success) {
            updateCartUI(data);
            if (data.cart_html) updateFullCartTable(data.cart_html);
            checkEmptyState(data.cart_count);
        }
    } catch (error) {
        console.error('[Cart] Update error:', error);
    }
}

/**
 * Actualiza los elementos comunes de la UI (Badges, Mini-Cart)
 */
function updateCartUI(data) {
    console.log('[Cart] Syncing UI with data:', data);
    
    // 1. Badges
    document.querySelectorAll('.cart-count-badge').forEach(badge => {
        badge.innerText = data.cart_count;
        badge.classList.toggle('hidden', data.cart_count === 0);
    });

    // 2. Mini Cart
    const miniCartContent = document.getElementById('mini-cart-content');
    if (miniCartContent && data.mini_cart_html) {
        miniCartContent.innerHTML = data.mini_cart_html;
    }
    
    // 3. Cart Page Headings
    const headerCount = document.getElementById('cart-header-count');
    if (headerCount) headerCount.innerText = `${data.cart_count} Productos`;

    // 4. Totals
    const subtotalEl = document.getElementById('cart-summary-subtotal');
    const totalEl = document.getElementById('cart-summary-total');
    if (subtotalEl) subtotalEl.innerText = `$${parseFloat(data.cart_subtotal).toLocaleString(undefined, {minimumFractionDigits: 2})}`;
    if (totalEl) totalEl.innerText = `$${parseFloat(data.cart_total).toLocaleString(undefined, {minimumFractionDigits: 2})}`;
}

/**
 * Inyecta el nuevo HTML de la tabla en la página de carrito
 */
function updateFullCartTable(html) {
    const container = document.getElementById('cart-table-container');
    if (container) {
        container.innerHTML = html;
        container.classList.add('animate-pulse');
        setTimeout(() => container.classList.remove('animate-pulse'), 400);
    }
}

/**
 * Muestra notificación Toast
 */
function showNotification(type, message) {
    const toast = document.createElement('div');
    const colors = { success: 'bg-green-500', error: 'bg-red-500', info: 'bg-blue-500' };
    toast.className = `fixed bottom-5 right-5 ${colors[type] || 'bg-gray-800'} text-white px-6 py-3 rounded-xl shadow-lg transform translate-y-10 opacity-0 transition-all duration-300 z-50 flex items-center gap-2 font-bold text-sm`;
    toast.innerHTML = `<span class="material-icons text-sm">info</span> ${message}`;
    document.body.appendChild(toast);
    setTimeout(() => toast.classList.remove('translate-y-10', 'opacity-0'), 10);
    setTimeout(() => {
        toast.classList.add('translate-y-10', 'opacity-0');
        setTimeout(() => toast.remove(), 300);
    }, 3000);
}

// Global Event Listeners (Delegation)
document.addEventListener('DOMContentLoaded', () => {
    console.log('Cart System Initialized');

    // Consolidated Delegated Event Listener for Clicks
    document.body.addEventListener('click', (e) => {
        const target = e.target;
        
        // 1. Add to Cart
        const addBtn = target.closest('.add-to-cart-btn');
        if (addBtn) {
            e.preventDefault();
            const quantitySpan = document.getElementById('quantity');
            const quantity = quantitySpan ? parseInt(quantitySpan.innerText) : 1;
            addToCart(addBtn.dataset.productId, quantity);
            return;
        }

        // 2. Quantity Update (+/-)
        const qtyBtn = target.closest('.qty-btn');
        if (qtyBtn) {
            e.preventDefault();
            updateCartItem(qtyBtn.dataset.itemId, qtyBtn.dataset.action);
            return;
        }

        // 3. Remove from Cart (Optional: converting to delegation)
        const removeBtn = target.closest('.remove-item-btn');
        if (removeBtn) {
            e.preventDefault();
            removeFromCart(removeBtn.dataset.itemId);
            return;
        }
    });

    // Toggle Mini Cart
    const toggleBtn = document.getElementById('cart-toggle-btn');
    const miniCart = document.getElementById('mini-cart-dropdown');
    
    if (toggleBtn && miniCart) {
        toggleBtn.addEventListener('click', (e) => {
            e.stopPropagation();
            const isHidden = miniCart.classList.contains('hidden');
            if (isHidden) {
                miniCart.classList.remove('hidden');
                requestAnimationFrame(() => {
                    miniCart.classList.remove('opacity-0', 'scale-95');
                    miniCart.classList.add('opacity-100', 'scale-100');
                });
            } else {
                miniCart.classList.add('opacity-0', 'scale-95');
                miniCart.classList.remove('opacity-100', 'scale-100');
                setTimeout(() => miniCart.classList.add('hidden'), 200);
            }
        });

        document.addEventListener('click', (e) => {
            if (!miniCart.classList.contains('hidden') && !miniCart.contains(e.target) && !toggleBtn.contains(e.target)) {
                miniCart.classList.add('opacity-0', 'scale-95');
                miniCart.classList.remove('opacity-100', 'scale-100');
                setTimeout(() => miniCart.classList.add('hidden'), 200);
            }
        });
    }
});
