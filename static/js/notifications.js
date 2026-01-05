/**
 * notifications.js
 * Sistema de Toasts Premium tipo Apple/Xiaomi
 */

function showToast(message, type = 'info') {
    const container = document.getElementById('toast-container') || createToastContainer();
    
    const toast = document.createElement('div');
    toast.className = `
        flex items-center gap-3 px-5 py-4 rounded-2xl shadow-2xl 
        transform translate-y-full opacity-0 transition-all duration-500 ease-out 
        border backdrop-blur-md font-display min-w-[300px]
    `;

    // Modern color schemes
    const styles = {
        success: 'bg-green-500 text-white border-green-400',
        error: 'bg-red-500 text-white border-red-400',
        info: 'bg-white/90 dark:bg-card-dark text-gray-900 dark:text-white border-gray-100 dark:border-gray-800',
        warning: 'bg-orange-500 text-white border-orange-400'
    };

    const icons = {
        success: 'check_circle',
        error: 'error',
        info: 'info',
        warning: 'warning'
    };

    toast.classList.add(...styles[type].split(' '));
    
    toast.innerHTML = `
        <div class="flex-shrink-0 w-8 h-8 rounded-full bg-white/20 flex items-center justify-center">
            <span class="material-icons text-xl">${icons[type]}</span>
        </div>
        <div class="flex-1">
            <p class="text-sm font-bold leading-tight">${message}</p>
        </div>
        <button class="ml-2 hover:opacity-70 transition-opacity">
            <span class="material-icons text-lg">close</span>
        </button>
    `;

    container.appendChild(toast);

    // Animate In
    setTimeout(() => {
        toast.classList.remove('translate-y-full', 'opacity-0');
    }, 10);

    // Auto Remove
    const removeTimer = setTimeout(() => {
        hideToast(toast);
    }, 5000);

    // Close button logic
    toast.querySelector('button').onclick = () => {
        clearTimeout(removeTimer);
        hideToast(toast);
    };
}

function hideToast(toast) {
    toast.classList.add('translate-y-full', 'opacity-0');
    setTimeout(() => toast.remove(), 500);
}

function createToastContainer() {
    const container = document.createElement('div');
    container.id = 'toast-container';
    container.className = 'fixed bottom-8 left-1/2 -translate-x-1/2 z-[300] flex flex-col items-center gap-3 w-full max-w-sm px-4';
    document.body.appendChild(container);
    return container;
}

// Map old global notifications if any
window.showNotification = showToast;
