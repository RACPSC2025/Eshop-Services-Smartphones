/**
 * State Management System - Replacement for Zustand
 * Implements reactive state with localStorage persistence
 */

// Initial Mock Data
const INITIAL_PRODUCTS = [
  {
    id: 1,
    name: "Xiaomi 14 Ultra",
    description: "<p>Experimenta la <strong>leyenda óptica</strong> con el Xiaomi 14 Ultra.</p>",
    price: 999.00,
    image: "https://i01.appmifile.com/v1/MI_18455B3E4DA706226CF7535A58E875F0267/pms_1708611224.28114676.png",
    category_id: 101,
    tag: "Flagship",
    rating: 5,
    catalog_type: "Smartphone"
  },
  {
    id: 2,
    name: "Redmi Note 13 Pro+",
    description: "<p>El rey de la gama media ha vuelto.</p>",
    price: 399.00,
    image: "https://i01.appmifile.com/v1/MI_18455B3E4DA706226CF7535A58E875F0267/pms_1705307374.88126760.png",
    category_id: 102,
    tag: "Bestseller",
    rating: 4.5,
    catalog_type: "Smartphone"
  },
  {
    id: 3,
    name: "Desbloqueo Cuenta Mi",
    description: "<p>Servicio remoto de desbloqueo oficial.</p>",
    price: 25.00,
    image: "https://cdn-icons-png.flaticon.com/512/3064/3064197.png",
    category_id: 201,
    tag: "Servicio",
    rating: 4.8,
    catalog_type: "Service"
  },
  {
    id: 4,
    name: "Poco X6 Pro 5G",
    description: "<p>Potencia bruta para gamers.</p>",
    price: 320.00,
    image: "https://i01.appmifile.com/v1/MI_18455B3E4DA706226CF7535A58E875F0267/pms_1705912497.03923594.png",
    category_id: 103,
    tag: "Gaming",
    rating: 4.7,
    catalog_type: "Smartphone"
  }
];

const INITIAL_USERS = [
  {
    id: 1,
    firstName: "Rac",
    lastName: "IA",
    email: "rac.ia.2025@gmail.com",
    joinDate: "Ene 2026",
    ordersCount: 2,
    points: 150,
    role: 'Admin',
    status: 'Active'
  },
  {
    id: 2,
    firstName: "Jason",
    lastName: "Ranti",
    email: "jason.r@example.com",
    joinDate: "Feb 2026",
    ordersCount: 5,
    points: 400,
    role: 'User',
    status: 'Active',
    avatar: 'https://i.pravatar.cc/150?u=jason'
  }
];

const INITIAL_ABOUT_DATA = {
  seo: {
    metaTitle: 'Nosotros | MiXiaomiUnlock - Expertos en Servicios Xiaomi',
    metaDescription: 'Conoce a los líderes en desbloqueo y soporte técnico para dispositivos Xiaomi en Latinoamérica. Garantía y seguridad.',
    keywords: 'nosotros, equipo xiaomi, soporte tecnico, desbloqueo xiaomi'
  },
  hero: {
    badge: 'Desde 2015',
    titleStart: 'Redefiniendo el',
    titleHighlight: 'Soporte Técnico',
    description: 'TechPro Solutions nació con una misión simple: hacer que la reparación de tecnología sea transparente, rápida y confiable. Hoy somos líderes en soluciones de software y hardware.'
  },
  stats: [
    { value: '50k+', label: 'Dispositivos Reparados' },
    { value: '99%', label: 'Tasa de Éxito' },
    { value: '24/7', label: 'Soporte Remoto' },
    { value: '4.9', label: 'Calificación Promedio' }
  ],
  story: {
    image: 'https://static.vecteezy.com/system/resources/previews/000/664/437/original/abstract-geometric-banner-with-orange-shapes.jpg',
    quote: 'La tecnología no debe ser un obstáculo, sino una herramienta.',
    title: 'Expertos en lo Imposible',
    description: 'Nos especializamos en lo que otros llaman "irreparable". Desde micro-soldadura en placas base hasta desbloqueos complejos de software remoto. Nuestro equipo está compuesto por ingenieros certificados apasionados por devolverle la vida a tus dispositivos.',
    points: [
      'Certificaciones Oficiales (Samsung, Apple, Xiaomi)',
      'Laboratorio con tecnología anti-estática',
      'Garantía de 90 días en todas las reparaciones',
      'Transparencia total en precios y diagnósticos'
    ]
  },
  team: [
    { id: 1, name: 'Carlos Ruiz', role: 'Ingeniero Jefe', image: 'https://images.unsplash.com/photo-1560250097-0b93528c311a?auto=format&fit=crop&q=80&w=300' },
    { id: 2, name: 'Ana M. Polo', role: 'Especialista Software', image: 'https://images.unsplash.com/photo-1573496359142-b8d87734a5a2?auto=format&fit=crop&q=80&w=300' },
    { id: 3, name: 'David Chen', role: 'Micro-electrónica', image: 'https://images.unsplash.com/photo-1472099645785-5658abf4ff4e?auto=format&fit=crop&q=80&w=300' }
  ]
};

const INITIAL_CONTACT_DATA = {
  seo: {
    metaTitle: 'Contacto | MiXiaomiUnlock - Soporte 24/7',
    metaDescription: '¿Necesitas ayuda con tu dispositivo? Contáctanos para soporte técnico, cotizaciones y desbloqueos remotos.',
    keywords: 'contacto xiaomi, soporte, ayuda, whatsapp, ubicacion'
  },
  title: 'Hablemos de Tecnología',
  subtitle: '¿Tienes un dispositivo roto, bloqueado o necesitas asesoría? Estamos aquí para ayudarte 24/7.',
  phone: '+52 (555) 123-4567',
  email: 'soporte@mixiaomi.com',
  address: 'Av. Reforma 222, CDMX',
  schedule: 'Lunes a Viernes, 9am - 6pm',
  mapImage: 'https://images.unsplash.com/photo-1524661135-423995f22d0b?auto=format&fit=crop&q=80&w=800'
};

const INITIAL_GALLERY_ITEMS = [
  {
    id: 'unlock-hero',
    title: 'Desbloqueo Oficial',
    subtitle: 'Recupera el acceso a tu dispositivo al instante.',
    image: 'https://images.unsplash.com/photo-1550751827-4bd374c3f58b?auto=format&fit=crop&q=80&w=1080',
    isHero: true
  },
  {
    id: 'main-hero',
    title: 'Xiaomi 14 Ultra',
    subtitle: 'La leyenda óptica con Leica.',
    image: 'https://i01.appmifile.com/v1/MI_18455B3E4DA706226CF7535A58E875F0267/pms_1708611224.28114676.png',
  },
  {
    id: 'hyperos',
    title: 'HyperOS',
    subtitle: 'Ecosistema Conectado.',
    image: 'https://miuirom.org/wp-content/uploads/2023/10/Xiaomi-HyperOS-1.jpg',
  },
  {
    id: 'cyberdog',
    title: 'CyberDog 2',
    subtitle: 'Inteligencia futura.',
    image: 'https://i01.appmifile.com/webfile/globalimg/products/pc/cyberdog-2/section01-header-m.webp',
  },
  {
    id: 'chipset',
    title: 'Snapdragon 8 Gen 3',
    subtitle: 'Potencia bruta.',
    image: 'https://images.unsplash.com/photo-1591488320449-011701bb6704?auto=format&fit=crop&q=80&w=1080',
  }
];

const INITIAL_BANNER_SLIDES = [
  {
    id: 1,
    badge: 'CERTIFICADO',
    badgeClass: 'bg-orange-500/20 text-orange-400 border-orange-500/30',
    titleStart: 'Servicio Oficial',
    titleEnd: 'Xiaomi & Poco',
    description: 'Recuperación de software y reparación de hardware con garantía de fábrica.',
    primaryBtn: 'Ver Catálogo',
    image: 'https://images.unsplash.com/photo-1598965402089-897ce52e8355?q=80&w=2832&auto=format&fit=crop',
    mediaType: 'image',
    bgClass: 'bg-black'
  },
  {
    id: 2,
    badge: 'PREMIUM',
    badgeClass: 'bg-blue-500/20 text-blue-400 border-blue-500/30',
    titleStart: 'Desbloqueo',
    titleEnd: 'Seguro & Rápido',
    description: 'Soluciones para cuentas Mi y FRP sin riesgos. Recupera tu dispositivo hoy.',
    primaryBtn: 'Empezar Ahora',
    image: 'https://assets.mixkit.co/videos/preview/mixkit-circuit-board-technology-1563-large.mp4',
    mediaType: 'video',
    bgClass: 'bg-[#0F172A]'
  }
];

const INITIAL_FOLDERS = [
  { id: '1', name: 'Descargas', parentId: null, createdAt: new Date().toISOString() },
  { id: '2', name: 'Facturas', parentId: null, createdAt: new Date().toISOString() },
  { id: '3', name: 'Documentos Clientes', parentId: null, createdAt: new Date().toISOString() },
];

// State Storage Key
const STORAGE_KEY = 'mixiaomi-storage-v1';

// Create Reactive State
class AppState {
  constructor() {
    this.subscribers = new Set();
    this.data = this.getInitialState();
    
    // Create proxy for reactivity
    this.state = new Proxy(this.data, {
      set: (target, property, value) => {
        target[property] = value;
        this.save();
        this.notify();
        return true;
      }
    });
  }

  getInitialState() {
    // Try to load from localStorage
    const stored = localStorage.getItem(STORAGE_KEY);
    if (stored) {
      try {
        return JSON.parse(stored);
      } catch (e) {
        console.warn('Failed to parse stored state, using defaults');
      }
    }

    // Return default state
    return {
      products: INITIAL_PRODUCTS,
      users: INITIAL_USERS,
      currentUser: null,
      cart: [],
      orders: [],
      notifications: [],
      favorites: [],
      aboutData: INITIAL_ABOUT_DATA,
      contactData: INITIAL_CONTACT_DATA,
      galleryItems: INITIAL_GALLERY_ITEMS,
      bannerSlides: INITIAL_BANNER_SLIDES,
      storedFiles: [],
      storedFolders: INITIAL_FOLDERS,
      adminHasNewOrder: false
    };
  }

  subscribe(callback) {
    this.subscribers.add(callback);
    return () => this.subscribers.delete(callback);
  }

  notify() {
    this.subscribers.forEach(callback => callback(this.state));
  }

  save() {
    try {
      localStorage.setItem(STORAGE_KEY, JSON.stringify(this.data));
    } catch (e) {
      console.error('Failed to save state to localStorage:', e);
    }
  }

  // Getters
  get(key) {
    return this.state[key];
  }

  // Setters
  set(key, value) {
    this.state[key] = value;
  }

  // Cart Actions
  addToCart(product, quantity) {
    const cart = [...this.state.cart];
    const existing = cart.find(item => item.id === product.id);
    
    if (existing) {
      existing.quantity += quantity;
    } else {
      cart.push({ ...product, quantity });
    }
    
    this.state.cart = cart;
  }

  removeFromCart(id) {
    this.state.cart = this.state.cart.filter(item => item.id !== id);
  }

  updateCartQty(id, delta) {
    this.state.cart = this.state.cart.map(item => {
      if (item.id === id) {
        const newQty = item.quantity + delta;
        return newQty > 0 ? { ...item, quantity: newQty } : item;
      }
      return item;
    });
  }

  clearCart() {
    this.state.cart = [];
  }

  // Order Actions
  addOrder(order) {
    this.state.orders = [order, ...this.state.orders];
    this.state.adminHasNewOrder = true;
  }

  updateOrderStatus(orderId, status) {
    const order = this.state.orders.find(o => o.id === orderId);
    
    this.state.orders = this.state.orders.map(o => 
      o.id === orderId ? { ...o, status } : o
    );

    // Add notification for user
    if (order) {
      const statusText = status === 'Processing' ? 'Procesando' : 
                        status === 'Completed' ? 'Completado' : 'Cancelado';
      
      const notification = {
        id: Date.now(),
        userId: order.userId,
        title: 'Actualización de Pedido',
        message: `Tu pedido #${order.id} está ahora: ${statusText}.`,
        read: false,
        date: new Date().toISOString(),
        type: 'order_update',
        linkTo: 'orders'
      };
      
      this.state.notifications = [notification, ...this.state.notifications];
    }
  }

  addOrderReview(orderId, rating, comment) {
    this.state.orders = this.state.orders.map(o => 
      o.id === orderId ? { 
        ...o, 
        userReview: { rating, comment, date: new Date().toISOString() }
      } : o
    );
  }

  setAdminHasNewOrder(val) {
    this.state.adminHasNewOrder = val;
  }

  // Notification Actions
  addNotification(notification) {
    this.state.notifications = [notification, ...this.state.notifications];
  }

  markNotificationsAsRead(userId) {
    this.state.notifications = this.state.notifications.map(n => 
      n.userId === userId ? { ...n, read: true } : n
    );
  }

  // Favorites
  toggleFavorite(productId) {
    const favorites = [...this.state.favorites];
    const index = favorites.indexOf(productId);
    
    if (index > -1) {
      favorites.splice(index, 1);
    } else {
      favorites.push(productId);
    }
    
    this.state.favorites = favorites;
  }

  // Product Actions
  addProduct(product) {
    this.state.products = [...this.state.products, product];
  }

  updateProduct(id, updates) {
    this.state.products = this.state.products.map(p => 
      p.id === id ? { ...p, ...updates } : p
    );
  }

  deleteProduct(id) {
    this.state.products = this.state.products.filter(p => p.id !== id);
  }

  // User Actions
  addUser(user) {
    this.state.users = [...this.state.users, user];
  }

  updateUser(id, updates) {
    this.state.users = this.state.users.map(u => 
      u.id === id ? { ...u, ...updates } : u
    );
  }

  deleteUser(id) {
    this.state.users = this.state.users.filter(u => u.id !== id);
  }

  setCurrentUser(user) {
    this.state.currentUser = user;
  }

  // Content Actions
  setAboutData(data) {
    this.state.aboutData = data;
  }

  setContactData(data) {
    this.state.contactData = data;
  }

  setGalleryItems(items) {
    this.state.galleryItems = items;
  }

  setBannerSlides(slides) {
    this.state.bannerSlides = slides;
  }

  // File Manager Actions
  addFile(file) {
    this.state.storedFiles = [...this.state.storedFiles, file];
  }

  createFolder(name, parentId) {
    const folder = {
      id: Date.now().toString(),
      name,
      parentId,
      createdAt: new Date().toISOString()
    };
    this.state.storedFolders = [...this.state.storedFolders, folder];
  }

  deleteFile(id) {
    this.state.storedFiles = this.state.storedFiles.filter(f => f.id !== id);
  }

  deleteFolder(id) {
    this.state.storedFolders = this.state.storedFolders.filter(f => f.id !== id);
    this.state.storedFiles = this.state.storedFiles.filter(f => f.folderId !== id);
  }
}

// Create and export global state instance
const appState = new AppState();
window.appState = appState;

export default appState;
