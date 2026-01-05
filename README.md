# Structure Folder

├─ core/ # Configuración principal (settings, urls, wsgi)
├─ apps/ # Carpeta contenedora de aplicaciones
│ ├─ products/ # Gestión de servicios (catalog, details)
│ ├─ orders/ # Gestión de carrito y checkout
│ ├─ users/ # Perfiles y autenticación (auth, profile)
│ └─ pages/ # Páginas estáticas (home, about, contact)
├─ static/ # Archivos CSS, JS, Imágenes globales
├─ templates/ # Templates compartidos (base.html)
│ ├─ components/ # Fragmentos (navbar, footer)
│ └─ ... (ver abajo)
├─ manage.py
└─ .env # Variables sensibles (DB, Secret Key)
