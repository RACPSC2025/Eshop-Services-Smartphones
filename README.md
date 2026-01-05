# Structure Folder

```text
├─ core/ # Configuración principal (settings, urls, wsgi)
├─ apps/ # Carpeta contenedora de aplicaciones
│ ├─ products/ # Gestión de servicios (catalog, details)
│ ├─ orders/ # Gestión de carrito y checkout
│ ├─ users/ # Perfiles y autenticación (auth, profile)
│ └─ pages/ # Páginas estáticas (home, about, contact)
├─ static/ # Archivos CSS, JS, Imágenes globales
templates/
├── components/ # navbar, footer, etc.
│ ├── footer.html
│ └── navbar.html
├── base.html # Template principal (base)
├── pages/ # Templates para la app 'pages'
│ ├── about.html
│ ├── contact.html
│ └── home.html
├── users/ # Templates para la app 'users'
│ ├── auth.html
│ └── profile.html
├── products/ # Templates para la app 'products'
│ ├── catalog.html
│ └── details.html
└── orders/ # Templates para la app 'orders'
| ├── cart.html
| └── checkout.html
├─ manage.py
└─ .env # Variables sensibles (DB, Secret Key)
```
