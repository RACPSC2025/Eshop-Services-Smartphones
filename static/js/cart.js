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

const csrftoken = getCookie('csrftoken');

/**
 * Agrega un producto al carrito
 * @param {number} productId 
 */
async function addToCart(productId) {
    try {
        const response = await fetch(`/orders/api/add/${productId}/`, {
            method: 'POST',
            headers: {
                'X-CSRFToken': csrftoken,
                'Content-Type': 'application/json'
            }
        });

        // 🛑 Guest restriction check
        if (response.status === 403) {
            const data = await response.json();
            if (data.error === 'login_required') {
                if (typeof openLoginModal === 'function') {
                    openLoginModal();
                } else {
                    window.location.href = '/users/auth/';
                }
                return;
            }
        }

        const data = await response.json();

        if (data.success) {
            updateCartUI(data);
            showNotification('success', data.message);
            // ... mini cart auto-open logic ...
        }
    } catch (error) {
        console.error('Error:', error);
    }
}

/**
 * Elimina un item del carrito
 * @param {number} itemId 
 */
async function removeFromCart(itemId) {
    try {
        const response = await fetch(`/orders/api/remove/${itemId}/`, {
            method: 'POST',
            headers: { 'X-CSRFToken': csrftoken }
        });

        const data = await response.json();

        if (data.success) {
            updateCartUI(data);
            if(data.cart_html) updateFullCartTable(data.cart_html); // Si estamos en page cart
            showNotification('info', data.message);
            
            // Si el carrito se vació en la página full, recargar para mostrar empty state
            if (data.cart_count === 0 && document.getElementById('cart-items-container')) {
                location.reload();
            }

        } else {
            showNotification('error', 'Error al eliminar');
        }
    } catch (error) {
        console.error(error);
    }
}

/**
 * Actualiza la cantidad de un item (+/-)
 * @param {number} itemId 
 * @param {string} action 'increase' or 'decrease'
 */
async function updateCartItem(itemId, action) {
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
            if(data.cart_html) updateFullCartTable(data.cart_html);
            
        }
    } catch (error) {
        console.error(error);
    }
}

/**
 * Actualiza los elementos comunes de la UI (Badges, Mini-Cart)
 */
function updateCartUI(data) {
    // 1. Update Badge Counts
    const badges = document.querySelectorAll('.cart-count-badge');
    badges.forEach(badge => {
        badge.innerText = data.cart_count;
        // Ocultar si es 0
        if(data.cart_count > 0) badge.classList.remove('hidden');
        else badge.classList.add('hidden');
    });

    // 2. Update Mini Cart HTML
    const miniCartContent = document.getElementById('mini-cart-content');
    if (miniCartContent && data.mini_cart_html) {
        miniCartContent.innerHTML = data.mini_cart_html;
    }
    
    // 3. Update Summary Totals (if on full page)
    if(document.getElementById('cart-summary-subtotal')) {
        document.getElementById('cart-summary-subtotal').innerText = `$${data.cart_subtotal}`;
        document.getElementById('cart-summary-tax').innerText = `$${data.cart_tax}`;
        document.getElementById('cart-summary-total').innerText = `$${data.cart_total}`;
    }
}

/**
 * Inyecta el nuevo HTML de la tabla en la página de carrito
 */
function updateFullCartTable(html) {
    const container = document.getElementById('cart-items-container');
    if(container) {
        container.innerHTML = html;
        container.classList.add('animate-pulse'); // Efecto visual
        setTimeout(() => container.classList.remove('animate-pulse'), 500);
    }
}

/**
 * Muestra notificación Toast
 */
function showNotification(type, message) {
    // Crear elemento
    const toast = document.createElement('div');
    const bgColor = type === 'success' ? 'bg-green-500' : type === 'error' ? 'bg-red-500' : 'bg-blue-500';
    
    toast.className = `fixed bottom-5 right-5 ${bgColor} text-white px-6 py-3 rounded-xl shadow-lg transform translate-y-10 opacity-0 transition-all duration-300 z-50 flex items-center gap-2 font-bold text-sm`;
    toast.innerHTML = `
        <span class="material-icons text-sm">${type === 'success' ? 'check_circle' : 'info'}</span>
        ${message}
    `;
    
    document.body.appendChild(toast);
    
    // Animate In
    setTimeout(() => {
        toast.classList.remove('translate-y-10', 'opacity-0');
    }, 10);
    
    // Remove after 3s
    setTimeout(() => {
        toast.classList.add('translate-y-10', 'opacity-0');
        setTimeout(() => toast.remove(), 300);
    }, 3000);
}

// Global Event Listeners (Delegation)
document.addEventListener('DOMContentLoaded', () => {
    console.log('Cart JS Loaded');

    // Add to Cart Buttons
    document.body.addEventListener('click', (e) => {
        const btn = e.target.closest('.add-to-cart-btn');
        if (btn) {
            e.preventDefault(); // Prevenir navegación si es un <a> o submit
            const productId = btn.dataset.productId;
            console.log('Add to cart clicked:', productId);
            if(productId) addToCart(productId);
        }
    });

    // Toggle Mini Cart
    const toggleBtn = document.getElementById('cart-toggle-btn');
    const miniCart = document.getElementById('mini-cart-dropdown');
    
    if (toggleBtn && miniCart) {
        toggleBtn.addEventListener('click', (e) => {
            e.stopPropagation();
            const isHidden = miniCart.classList.contains('hidden');
            console.log('Cart Toggle Clicked. Is hidden?', isHidden);
            
            if (isHidden) {
                miniCart.classList.remove('hidden');
                // Small delay to allow display:block to apply before transition
                requestAnimationFrame(() => {
                    miniCart.classList.remove('opacity-0', 'scale-95');
                    miniCart.classList.add('opacity-100', 'scale-100');
                });
            } else {
                miniCart.classList.add('opacity-0', 'scale-95');
                miniCart.classList.remove('opacity-100', 'scale-100');
                
                // Wait for transition to finish
                setTimeout(() => {
                    miniCart.classList.add('hidden');
                }, 200);
            }
        });

        // Close when clicking outside
        document.addEventListener('click', (e) => {
            if (!miniCart.classList.contains('hidden') && !miniCart.contains(e.target) && !toggleBtn.contains(e.target)) {
                miniCart.classList.add('opacity-0', 'scale-95');
                miniCart.classList.remove('opacity-100', 'scale-100');
                setTimeout(() => {
                    miniCart.classList.add('hidden');
                }, 200);
            }
        });
    } else {
        console.error('Cart toggle elements NOT found in DOM');
    }
});

