document.addEventListener('DOMContentLoaded', () => {
    // Selectores para el control de cantidad en la página de detalles
    const minusBtn = document.querySelector('.qty-minus');
    const plusBtn = document.querySelector('.qty-plus');
    const quantitySpan = document.getElementById('quantity');

    if (!quantitySpan || !minusBtn || !plusBtn) return;
    
    let quantity = 1;

    function updateQuantityDisplay() {
        quantitySpan.textContent = quantity;
    }

    minusBtn.addEventListener('click', () => {
        if (quantity > 1) {
            quantity--;
            updateQuantityDisplay();
        }
    });

    plusBtn.addEventListener('click', () => {
        quantity++;
        updateQuantityDisplay();
    });

    // El evento 'click' para .add-to-cart-btn ahora es manejado por delegación en cart.js
});