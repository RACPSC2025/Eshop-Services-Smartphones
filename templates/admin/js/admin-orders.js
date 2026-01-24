/**
 * Admin Orders Management
 */
const AdminOrders = {
    init() {
        this.tableBody = document.getElementById('orders-table-body');
        this.filterBtns = document.querySelectorAll('.filter-btn');
        this.currentFilter = 'all';
        
        if (!this.tableBody) return;

        this.renderOrders();
        this.setupEventListeners();
        
        if (window.appState) {
            window.appState.subscribe(() => this.renderOrders());
        }
    },

    renderOrders() {
        const orders = window.appState ? window.appState.get('orders') : [];
        const users = window.appState ? window.appState.get('users') : [];
        
        let filteredOrders = orders;
        if (this.currentFilter === 'pending') {
            filteredOrders = orders.filter(o => o.status === 'Pending' || o.status === 'Processing');
        } else if (this.currentFilter === 'completed') {
            filteredOrders = orders.filter(o => o.status === 'Completed');
        }

        this.tableBody.innerHTML = filteredOrders.length > 0 ? filteredOrders.map(order => {
            const user = users.find(u => u.id === order.userId) || { firstName: 'User', lastName: order.userId };
            const statusMap = {
                'Pending': { label: 'Pendiente', class: 'bg-yellow-100 text-yellow-700' },
                'Processing': { label: 'Procesando', class: 'bg-blue-100 text-blue-700' },
                'Completed': { label: 'Completado', class: 'bg-green-100 text-green-700' },
                'Cancelled': { label: 'Cancelado', class: 'bg-red-100 text-red-700' }
            };
            const status = statusMap[order.status] || { label: order.status, class: 'bg-gray-100 text-gray-700' };

            return `
                <tr class="hover:bg-gray-50 transition-colors">
                    <td class="px-6 py-4 font-bold text-gray-900">#${order.id}</td>
                    <td class="px-6 py-4">
                        <div class="flex items-center gap-3">
                            <div class="w-8 h-8 rounded-full bg-blue-100 flex items-center justify-center text-blue-600 text-xs font-bold">
                                ${user.firstName[0]}${user.lastName[0]}
                            </div>
                            <span class="text-sm font-medium">${user.firstName} ${user.lastName}</span>
                        </div>
                    </td>
                    <td class="px-6 py-4 text-sm text-gray-500">
                        ${this.formatDate(order.date)}
                    </td>
                    <td class="px-6 py-4 font-bold text-gray-900">$${order.total.toFixed(2)}</td>
                    <td class="px-6 py-4">
                        <span class="px-3 py-1 ${status.class} text-xs font-bold rounded-full">
                            ${status.label}
                        </span>
                    </td>
                    <td class="px-6 py-4 text-right">
                        <button onclick="AdminOrders.viewOrder('${order.id}')" class="p-2 text-gray-400 hover:text-xiaomi transition-colors">
                            <span class="material-icons text-sm">visibility</span>
                        </button>
                    </td>
                </tr>
            `;
        }).join('') : `
            <tr>
                <td colspan="6" class="px-6 py-12 text-center text-gray-500">
                    <span class="material-icons text-4xl block mb-2 opacity-20">shopping_bag</span>
                    No hay pedidos que coincidan con el filtro.
                </td>
            </tr>
        `;
    },

    setupEventListeners() {
        this.filterBtns.forEach(btn => {
            btn.addEventListener('click', () => {
                // Update UI classes
                this.filterBtns.forEach(b => {
                    b.classList.remove('bg-xiaomi', 'text-white');
                    b.classList.add('text-gray-600', 'hover:bg-gray-50');
                });
                btn.classList.add('bg-xiaomi', 'text-white');
                btn.classList.remove('text-gray-600', 'hover:bg-gray-50');

                // Update Filter
                if (btn.id === 'filter-all') this.currentFilter = 'all';
                if (btn.id === 'filter-pending') this.currentFilter = 'pending';
                if (btn.id === 'filter-completed') this.currentFilter = 'completed';

                this.renderOrders();
            });
        });
    },

    viewOrder(id) {
        console.log('View order:', id);
        // TODO: Open order details modal
    },

    formatDate(dateStr) {
        const date = new Date(dateStr);
        if (isNaN(date)) return 'Reciente';
        return date.toLocaleDateString();
    }
};

document.addEventListener('DOMContentLoaded', () => {
    AdminOrders.init();
});

window.AdminOrders = AdminOrders;
