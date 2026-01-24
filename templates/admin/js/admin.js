/**
 * AdminDashboard Layout & Global Logic
 */
window.AdminDashboard = {
    init() {
        console.log('Admin Dashboard Initialized');
        this.highlightActiveLink();
        this.setupLogout();
        this.loadStats();
        this.renderRecentOrders();
        
        if (window.appState) {
            window.appState.subscribe(() => {
                this.loadStats();
                this.renderRecentOrders();
            });
        }
    },

    highlightActiveLink() {
        const currentPath = window.location.pathname.split('/').pop() || 'dashboard.html';
        const navLinks = document.querySelectorAll('nav a');
        
        navLinks.forEach(link => {
            const href = link.getAttribute('href');
            // Remove active classes
            link.classList.remove('bg-xiaomi/10', 'text-xiaomi', 'font-bold');
            link.classList.add('text-gray-600', 'hover:bg-gray-50');

            if (href === currentPath || (currentPath === '' && href === 'dashboard.html')) {
                link.classList.add('bg-xiaomi/10', 'text-xiaomi', 'font-bold');
                link.classList.remove('text-gray-600', 'hover:bg-gray-50');
            }
        });
    },

    setupLogout() {
        const logoutBtn = document.querySelector('button:has(.material-icons:contains("logout"))') 
                          || Array.from(document.querySelectorAll('button')).find(btn => btn.textContent.includes('Cerrar Sesión'));
        
        if (logoutBtn) {
            logoutBtn.addEventListener('click', () => {
                if (confirm('¿Estás seguro de que deseas cerrar sesión?')) {
                    window.location.href = 'index.html';
                }
            });
        }
    },

    loadStats() {
        const products = window.appState ? window.appState.get('products') : [];
        const users = window.appState ? window.appState.get('users') : [];
        const orders = window.appState ? window.appState.get('orders') : [];
        
        const totalRevenue = orders.reduce((sum, order) => sum + (order.status === 'Completed' ? order.total : 0), 0);
        
        const elements = {
            revenue: document.getElementById('stat-revenue'),
            orders: document.getElementById('stat-orders'),
            users: document.getElementById('stat-users'),
            products: document.getElementById('stat-products')
        };

        if (elements.revenue) elements.revenue.textContent = `$${totalRevenue.toFixed(0)}`;
        if (elements.orders) elements.orders.textContent = orders.length;
        if (elements.users) elements.users.textContent = users.length;
        if (elements.products) elements.products.textContent = products.length;
    },

    renderRecentOrders() {
        const container = document.getElementById('recent-orders-list');
        if (!container) return;

        const orders = window.appState ? window.appState.get('orders') : [];
        const users = window.appState ? window.appState.get('users') : [];
        
        const recentOrders = [...orders].reverse().slice(0, 5);

        container.innerHTML = recentOrders.length > 0 ? recentOrders.map(order => {
            const user = users.find(u => u.id === order.userId) || { firstName: 'User', lastName: order.userId };
            const statusMap = {
                'Pending': { icon: 'shopping_bag', color: 'blue', labelClass: 'bg-yellow-100 text-yellow-700', label: 'Pendiente' },
                'Processing': { icon: 'sync', color: 'blue', labelClass: 'bg-blue-100 text-blue-700', label: 'Procesando' },
                'Completed': { icon: 'check_circle', color: 'green', labelClass: 'bg-green-100 text-green-700', label: 'Completado' },
                'Cancelled': { icon: 'cancel', color: 'red', labelClass: 'bg-red-100 text-red-700', label: 'Cancelado' }
            };
            const status = statusMap[order.status] || statusMap['Pending'];

            // Handle potential issues with Tailwind dynamic classes if not compiled
            // But we are using CDN tailwind which handles classes dynamically
            
            return `
                <div class="flex items-center gap-4 p-4 bg-gray-50 rounded-xl hover:bg-gray-100 transition-colors">
                    <div class="w-12 h-12 bg-${status.color}-100 rounded-xl flex items-center justify-center flex-shrink-0">
                        <span class="material-icons text-${status.color}-600">${status.icon}</span>
                    </div>
                    <div class="flex-1 min-w-0">
                        <p class="font-bold text-gray-900">Pedido #${order.id}</p>
                        <p class="text-sm text-gray-500">${user.firstName} ${user.lastName} • ${order.items || 1} item(s)</p>
                    </div>
                    <div class="text-right">
                        <p class="font-bold text-gray-900">$${order.total.toFixed(2)}</p>
                        <span class="inline-block px-3 py-1 ${status.labelClass} text-xs font-bold rounded-full">
                            ${status.label}
                        </span>
                    </div>
                </div>
            `;
        }).join('') : `
            <div class="p-8 text-center text-gray-400">
                No hay pedidos recientes.
            </div>
        `;
    }
};
