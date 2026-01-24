/**
 * Utility Functions
 * Helper functions used throughout the application
 */

/**
 * Create DOM element with props and children
 */
export function createElement(tag, props = {}, ...children) {
  const element = document.createElement(tag);
  
  // Set properties
  Object.entries(props).forEach(([key, value]) => {
    if (key === 'className') {
      element.className = value;
    } else if (key === 'onClick') {
      element.addEventListener('click', value);
    } else if (key.startsWith('on')) {
      const event = key.substring(2).toLowerCase();
      element.addEventListener(event, value);
    } else if (key === 'style' && typeof value === 'object') {
      Object.assign(element.style, value);
    } else {
      element.setAttribute(key, value);
    }
  });
  
  // Append children
  children.forEach(child => {
    if (typeof child === 'string') {
      element.appendChild(document.createTextNode(child));
    } else if (child instanceof Node) {
      element.appendChild(child);
    }
  });
  
  return element;
}

/**
 * Format currency
 */
export function formatCurrency(value) {
  return `$${value.toLocaleString('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 2 })}`;
}

/**
 * Format date
 */
export function formatDate(dateString) {
  const date = new Date(dateString);
  const options = { year: 'numeric', month: 'short', day: 'numeric' };
  return date.toLocaleDateString('es-ES', options);
}

/**
 * Generate unique ID
 */
export function generateId() {
  return Math.random().toString(36).substr(2, 9).toUpperCase();
}

/**
 * Sanitize HTML (basic implementation)
 */
export function sanitizeHTML(html) {
  const div = document.createElement('div');
  div.innerHTML = html;
  return div.innerHTML;
}

/**
 * Show toast notification
 */
export function showToast(message, type = 'success') {
  const toastContainer = document.getElementById('toast-container');
  if (!toastContainer) return;

  const toast = document.createElement('div');
  toast.className = `fixed top-24 right-6 z-[100] transition-all duration-500 transform translate-x-0 opacity-100`;
  
  const icon = type === 'success' ? 'shopping_cart' : 'info';
  const bgColor = type === 'success' ? 'border-xiaomi' : 'border-blue-500';
  
  toast.innerHTML = `
    <div class="bg-white ${bgColor} border-l-4 text-gray-900 pl-4 pr-6 py-4 rounded-r-xl shadow-2xl flex items-center gap-4 min-w-[300px]">
      <div class="bg-xiaomi/10 rounded-full p-2 text-xiaomi">
        <span class="material-icons text-xl">${icon}</span>
      </div>
      <div>
        <h4 class="font-bold text-sm">Notificación</h4>
        <span class="text-xs text-gray-500 font-medium">${message}</span>
      </div>
    </div>
  `;
  
  toastContainer.appendChild(toast);
  
  // Auto remove after 3 seconds
  setTimeout(() => {
    toast.style.transform = 'translateX(10px)';
    toast.style.opacity = '0';
    
    setTimeout(() => {
      if (toastContainer.contains(toast)) {
        toastContainer.removeChild(toast);
      }
    }, 500);
  }, 3000);
}

/**
 * Show modal
 */
export function showModal(content, onClose = null) {
  const modalContainer = document.getElementById('modal-container');
  if (!modalContainer) return;

  const modal = document.createElement('div');
  modal.className = 'fixed inset-0 z-[200] flex items-center justify-center p-4 bg-black/50 backdrop-blur-sm animate-fade-in';
  
  const modalBox = document.createElement('div');
  modalBox.className = 'bg-white rounded-3xl shadow-2xl max-w-2xl w-full max-h-[90vh] overflow-auto animate-scale-in';
  
  if (typeof content === 'string') {
    modalBox.innerHTML = content;
  } else if (content instanceof Node) {
    modalBox.appendChild(content);
  }
  
  modal.appendChild(modalBox);
  modalContainer.appendChild(modal);
  
  // Close on backdrop click
  modal.addEventListener('click', (e) => {
    if (e.target === modal) {
      closeModal();
      if (onClose) onClose();
    }
  });
  
  // Close with Escape key
  const handleEscape = (e) => {
    if (e.key === 'Escape') {
      closeModal();
      if (onClose) onClose();
      document.removeEventListener('keydown', handleEscape);
    }
  };
  document.addEventListener('keydown', handleEscape);
  
  function closeModal() {
    modal.style.opacity = '0';
    setTimeout(() => {
      if (modalContainer.contains(modal)) {
        modalContainer.removeChild(modal);
      }
    }, 300);
  }
  
  return { modal, close: closeModal };
}

/**
 * Hide modal
 */
export function hideModal() {
  const modalContainer = document.getElementById('modal-container');
  if (modalContainer) {
    modalContainer.innerHTML = '';
  }
}

/**
 * Flying cart animation
 */
export function triggerFlyingCartAnimation(event) {
  const cartIcon = document.getElementById('cart-icon-container');
  if (!cartIcon) return;

  const flyer = document.createElement('div');
  flyer.className = 'fixed z-[9999] w-10 h-10 bg-xiaomi rounded-full flex items-center justify-center text-white shadow-2xl pointer-events-none transition-all duration-1000';
  flyer.style.transitionTimingFunction = 'cubic-bezier(0.2, 1, 0.2, 1)';
  flyer.innerHTML = '<span class="material-icons text-lg">shopping_cart</span>';
  
  const startX = event.clientX;
  const startY = event.clientY;
  
  flyer.style.left = `${startX}px`;
  flyer.style.top = `${startY}px`;
  flyer.style.transform = 'translate(-50%, -50%) scale(0.5)';
  flyer.style.opacity = '0';

  document.body.appendChild(flyer);

  const targetRect = cartIcon.getBoundingClientRect();
  const targetX = targetRect.left + (targetRect.width / 2);
  const targetY = targetRect.top + (targetRect.height / 2);

  requestAnimationFrame(() => {
    flyer.style.opacity = '1';
    flyer.style.transform = 'translate(-50%, -50%) scale(1.2)';

    setTimeout(() => {
      flyer.style.left = `${targetX}px`;
      flyer.style.top = `${targetY}px`;
      flyer.style.transform = 'translate(-50%, -50%) scale(0.2)';
      flyer.style.opacity = '0.5';
    }, 100);
  });

  setTimeout(() => {
    if (document.body.contains(flyer)) {
      document.body.removeChild(flyer);
    }
  }, 1100);
}

/**
 * Debounce function
 */
export function debounce(func, wait) {
  let timeout;
  return function executedFunction(...args) {
    const later = () => {
      clearTimeout(timeout);
      func(...args);
    };
    clearTimeout(timeout);
    timeout = setTimeout(later, wait);
  };
}

/**
 * Get cart total
 */
export function getCartTotal(cart) {
  return cart.reduce((total, item) => total + (item.price * item.quantity), 0);
}

/**
 * Get cart item count
 */
export function getCartItemCount(cart) {
  return cart.reduce((count, item) => count + item.quantity, 0);
}

/**
 * Validate email
 */
export function validateEmail(email) {
  const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  return re.test(email);
}

/**
 * Validate required field
 */
export function validateRequired(value) {
  return value && value.trim().length > 0;
}

/**
 * Show loading skeleton
 */
export function showLoadingSkeleton(container, count = 4) {
  const skeleton = `
    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
      ${Array(count).fill('').map(() => `
        <div class="bg-white rounded-3xl p-6 animate-pulse">
          <div class="w-full h-48 bg-gray-200 rounded-2xl mb-4"></div>
          <div class="h-4 bg-gray-200 rounded w-3/4 mb-2"></div>
          <div class="h-4 bg-gray-200 rounded w-1/2"></div>
        </div>
      `).join('')}
    </div>
  `;
  
  if (container) {
    container.innerHTML = skeleton;
  }
}

/**
 * Escape HTML to prevent XSS
 */
export function escapeHTML(text) {
  const div = document.createElement('div');
  div.textContent = text;
  return div.innerHTML;
}

/**
 * Parse URL parameters
 */
export function parseURLParams() {
  const params = new URLSearchParams(window.location.search);
  const result = {};
  for (const [key, value] of params) {
    result[key] = value;
  }
  return result;
}

/**
 * Smooth scroll to element
 */
export function scrollToElement(elementId) {
  const element = document.getElementById(elementId);
  if (element) {
    element.scrollIntoView({ behavior: 'smooth', block: 'start' });
  }
}

/**
 * Copy to clipboard
 */
export async function copyToClipboard(text) {
  try {
    await navigator.clipboard.writeText(text);
    showToast('Copiado al portapapeles', 'success');
  } catch (err) {
    console.error('Failed to copy:', err);
    showToast('Error al copiar', 'error');
  }
}

/**
 * File size formatter
 */
export function formatFileSize(bytes) {
  if (bytes === 0) return '0 Bytes';
  const k = 1024;
  const sizes = ['Bytes', 'KB', 'MB', 'GB'];
  const i = Math.floor(Math.log(bytes) / Math.log(k));
  return Math.round(bytes / Math.pow(k, i) * 100) / 100 + ' ' + sizes[i];
}

/**
 * Read file as Base64
 */
export function readFileAsBase64(file) {
  return new Promise((resolve, reject) => {
    const reader = new FileReader();
    reader.onload = () => resolve(reader.result);
    reader.onerror = reject;
    reader.readAsDataURL(file);
  });
}

/**
 * Download file from base64
 */
export function downloadBase64File(base64, filename) {
  const link = document.createElement('a');
  link.href = base64;
  link.download = filename;
  document.body.appendChild(link);
  link.click();
  document.body.removeChild(link);
}

// Export all utilities as default object
export default {
  createElement,
  formatCurrency,
  formatDate,
  generateId,
  sanitizeHTML,
  showToast,
  showModal,
  hideModal,
  triggerFlyingCartAnimation,
  debounce,
  getCartTotal,
  getCartItemCount,
  validateEmail,
  validateRequired,
  showLoadingSkeleton,
  escapeHTML,
  parseURLParams,
  scrollToElement,
  copyToClipboard,
  formatFileSize,
  readFileAsBase64,
  downloadBase64File
};
