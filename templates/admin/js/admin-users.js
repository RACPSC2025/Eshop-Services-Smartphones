/**
 * Admin Users Management
 */
const AdminUsers = {
    init() {
        this.tableBody = document.getElementById('users-table-body');
        this.searchInput = document.getElementById('user-search');
        this.addBtn = document.getElementById('add-user-btn');
        this.modal = document.getElementById('user-modal');
        this.form = document.getElementById('user-form');
        
        if (!this.tableBody) return;

        this.renderUsers();
        this.setupEventListeners();
        
        if (window.appState) {
            window.appState.subscribe(() => this.renderUsers());
        }
    },

    renderUsers(filter = '') {
        const users = window.appState ? window.appState.get('users') : [];
        const filteredUsers = users.filter(u => 
            u.firstName.toLowerCase().includes(filter.toLowerCase()) ||
            u.lastName.toLowerCase().includes(filter.toLowerCase()) ||
            u.email.toLowerCase().includes(filter.toLowerCase()) ||
            u.id.toString().includes(filter)
        );

        this.tableBody.innerHTML = filteredUsers.map(user => `
            <tr class="hover:bg-gray-50 transition-colors">
                <td class="px-6 py-4">
                    <div class="flex items-center gap-3">
                        ${user.avatar ? `
                            <img src="${user.avatar}" class="w-10 h-10 rounded-full" />
                        ` : `
                            <div class="w-10 h-10 rounded-full bg-gradient-to-br from-xiaomi to-orange-600 flex items-center justify-center text-white font-bold">
                                ${user.firstName[0]}
                            </div>
                        `}
                        <div>
                            <p class="font-bold text-gray-900">${user.firstName} ${user.lastName}</p>
                            <p class="text-xs text-gray-400">#${user.id}</p>
                        </div>
                    </div>
                </td>
                <td class="px-6 py-4 text-gray-700">
                    ${user.email}
                </td>
                <td class="px-6 py-4">
                    <span class="px-3 py-1 ${user.role === 'Admin' ? 'bg-red-100 text-red-700' : 'bg-blue-100 text-blue-700'} text-xs font-bold rounded-full">
                        ${user.role}
                    </span>
                </td>
                <td class="px-6 py-4 font-bold">
                    ${user.points} pts
                </td>
                <td class="px-6 py-4">
                    <span class="px-3 py-1 bg-green-100 text-green-700 text-xs font-bold rounded-full">
                        ${user.status || 'Active'}
                    </span>
                </td>
                <td class="px-6 py-4">
                    <div class="flex items-center justify-end gap-2">
                        <button onclick="AdminUsers.editUser(${user.id})" class="p-2 text-blue-600 hover:bg-blue-50 rounded-lg transition-colors">
                            <span class="material-icons text-sm">edit</span>
                        </button>
                        <button onclick="AdminUsers.deleteUser(${user.id})" class="p-2 text-red-600 hover:bg-red-50 rounded-lg transition-colors">
                            <span class="material-icons text-sm">delete</span>
                        </button>
                    </div>
                </td>
            </tr>
        `).join('');
    },

    setupEventListeners() {
        if (this.searchInput) {
            this.searchInput.addEventListener('input', (e) => {
                this.renderUsers(e.target.value);
            });
        }

        if (this.addBtn) {
            this.addBtn.addEventListener('click', () => this.openAddModal());
        }

        if (this.form) {
            this.form.addEventListener('submit', (e) => this.handleFormSubmit(e));
        }
    },

    openAddModal() {
        document.getElementById('modal-title').textContent = 'Nuevo Usuario';
        this.form.reset();
        document.getElementById('user-id').value = '';
        this.modal.classList.remove('hidden');
    },

    closeModal() {
        this.modal.classList.add('hidden');
    },

    editUser(id) {
        const user = window.appState.get('users').find(u => u.id === id);
        if (!user) return;

        document.getElementById('modal-title').textContent = 'Editar Usuario';
        document.getElementById('user-id').value = user.id;
        document.getElementById('u-first').value = user.firstName;
        document.getElementById('u-last').value = user.lastName;
        document.getElementById('u-email').value = user.email;
        document.getElementById('u-role').value = user.role || 'User';
        document.getElementById('u-status').value = user.status || 'Active';

        this.modal.classList.remove('hidden');
    },

    handleFormSubmit(e) {
        e.preventDefault();
        const id = document.getElementById('user-id').value;
        const firstName = document.getElementById('u-first').value;
        const lastName = document.getElementById('u-last').value;
        const email = document.getElementById('u-email').value;
        const role = document.getElementById('u-role').value;
        const status = document.getElementById('u-status').value;

        const userData = {
            firstName,
            lastName,
            email,
            role,
            status,
            points: id ? undefined : 0,
            joinDate: id ? undefined : new Date().toLocaleDateString('es-ES', { month: 'short', year: 'numeric' })
        };

        if (id) {
            window.appState.updateUser(parseInt(id), userData);
        } else {
            userData.id = Date.now();
            window.appState.addUser(userData);
        }

        this.closeModal();
    },

    deleteUser(id) {
        if (confirm('¿Estás seguro de que deseas eliminar este usuario?')) {
            if (window.appState) {
                window.appState.deleteUser(id);
            }
        }
    }
};

document.addEventListener('DOMContentLoaded', () => {
    AdminUsers.init();
});

window.AdminUsers = AdminUsers;
