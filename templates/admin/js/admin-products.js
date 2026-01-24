/**
 * Admin Products Management
 */
const AdminProducts = {
    init() {
        this.tableBody = document.getElementById('products-table-body');
        this.searchInput = document.getElementById('product-search');
        this.addBtn = document.getElementById('add-product-btn');
        this.modal = document.getElementById('product-modal');
        this.form = document.getElementById('product-form');
        
        if (!this.tableBody) return;

        this.renderProducts();
        this.setupEventListeners();
        
        if (window.appState) {
            window.appState.subscribe(() => this.renderProducts());
        }
    },

    renderProducts(filter = '') {
        const products = window.appState ? window.appState.get('products') : [];
        const filteredProducts = products.filter(p => 
            p.name.toLowerCase().includes(filter.toLowerCase()) ||
            p.id.toString().includes(filter)
        );

        this.tableBody.innerHTML = filteredProducts.map(product => `
            <tr class="hover:bg-gray-50 transition-colors">
                <td class="px-6 py-4">
                    <div class="flex items-center gap-3">
                        <img
                            src="${product.image}"
                            alt="${product.name}"
                            class="w-12 h-12 object-contain bg-gray-50 rounded-lg p-1"
                        />
                        <div>
                            <p class="font-bold text-gray-900">${product.name}</p>
                            <p class="text-xs text-gray-400">ID: #${product.id.toString().padStart(3, '0')}</p>
                        </div>
                    </div>
                </td>
                <td class="px-6 py-4">
                    <span class="px-3 py-1 bg-orange-100 text-orange-700 text-xs font-bold rounded-full">
                        ${product.tag || 'General'}
                    </span>
                </td>
                <td class="px-6 py-4 font-bold text-gray-900">
                    $${product.price.toFixed(2)}
                </td>
                <td class="px-6 py-4">
                    <div class="flex items-center gap-1">
                        <span class="material-icons text-yellow-400 text-sm">star</span>
                        <span class="font-bold">${product.rating}</span>
                    </div>
                </td>
                <td class="px-6 py-4">
                    <span class="px-3 py-1 bg-green-100 text-green-700 text-xs font-bold rounded-full">
                        Activo
                    </span>
                </td>
                <td class="px-6 py-4">
                    <div class="flex items-center justify-end gap-2">
                        <button onclick="AdminProducts.editProduct(${product.id})" class="p-2 text-blue-600 hover:bg-blue-50 rounded-lg transition-colors">
                            <span class="material-icons text-sm">edit</span>
                        </button>
                        <button onclick="AdminProducts.deleteProduct(${product.id})" class="p-2 text-red-600 hover:bg-red-50 rounded-lg transition-colors">
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
                this.renderProducts(e.target.value);
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
        document.getElementById('modal-title').textContent = 'Nuevo Producto';
        this.form.reset();
        document.getElementById('product-id').value = '';
        this.modal.classList.remove('hidden');
    },

    closeModal() {
        this.modal.classList.add('hidden');
    },

    editProduct(id) {
        const product = window.appState.get('products').find(p => p.id === id);
        if (!product) return;

        document.getElementById('modal-title').textContent = 'Editar Producto';
        document.getElementById('product-id').value = product.id;
        document.getElementById('p-name').value = product.name;
        document.getElementById('p-price').value = product.price;
        document.getElementById('p-tag').value = product.tag || 'Flagship';
        document.getElementById('p-image').value = product.image;
        document.getElementById('p-description').value = product.description.replace(/<[^>]*>/g, '');

        this.modal.classList.remove('hidden');
    },

    handleFormSubmit(e) {
        e.preventDefault();
        const id = document.getElementById('product-id').value;
        const name = document.getElementById('p-name').value;
        const price = parseFloat(document.getElementById('p-price').value);
        const tag = document.getElementById('p-tag').value;
        const image = document.getElementById('p-image').value;
        const description = document.getElementById('p-description').value;

        const productData = {
            name,
            price,
            tag,
            image,
            description: `<p>${description}</p>`,
            catalog_type: tag === 'Servicio' ? 'Service' : 'Smartphone',
            rating: id ? undefined : 5.0 // Default rating for new products
        };

        if (id) {
            window.appState.updateProduct(parseInt(id), productData);
        } else {
            productData.id = Date.now();
            window.appState.addProduct(productData);
        }

        this.closeModal();
    },

    deleteProduct(id) {
        if (confirm('¿Estás seguro de que deseas eliminar este producto?')) {
            if (window.appState) {
                window.appState.deleteProduct(id);
            }
        }
    }
};

// Initialize when ready
document.addEventListener('DOMContentLoaded', () => {
    AdminProducts.init();
});

window.AdminProducts = AdminProducts;
