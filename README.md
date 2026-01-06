<div align="center">

<img src="static/assets/images/Mascota-Auth.png" alt="Mascota UnlockXiaomi" width="200" height="200" style="border-radius: 50%;">

# UnlockXiaomi - SERVICIO TÉCNICO GARANTIZADO

**Especialistas en desbloqueo, reparación y servicios técnicos certificados para dispositivos Xiaomi y Poco**

---

<span style="background: #F75A02; padding: 8px 15px; border-radius: 20px; color: white; font-weight: bold;">
  20min Tiempo Promedio | 90 días Garantía | 100% Éxito | 24/7 Soporte
</span>

</div>

# UnlockXiaomi Colombia - Plataforma E-commerce

**UnlockXiaomi Colombia** es una plataforma e-commerce premium especializada en servicios técnicos certificados y venta de productos para dispositivos Xiaomi, Samsung y más.

El proyecto utiliza tecnologías de vanguardia: Django 6.0, Tailwind CSS 4.1.18, PostgreSQL y Python 3.11+.

## 🚀 Stack Tecnológico

### Backend

- **Framework:** Django 6.0 (última versión)
- **Python:** 3.11+
- **Base de datos:** PostgreSQL 15/16
- **Gestor de entornos:** virtualenvwrapper (workon)
- **Dependencias principales:**
  - `django-tailwind-cli==4.5.1`
  - `gunicorn>=23.0.0`
  - `pillow==12.1.0` (procesamiento de imágenes)
  - `psycopg[binary]==3.3.2` (driver PostgreSQL)
  - `python-dotenv==1.2.1`
  - `django-allauth==65.13.1` (autenticación)

### Frontend

- **CSS Framework:** Tailwind CSS 4.1.18 (Motor Oxide - Rust)
- **Fuentes:** Inter, Poppins (Google Fonts)
- **Iconos:** Material Icons
- **Vanilla JavaScript** para interactividad

## 📁 Arquitectura del Proyecto

### Estructura de Directorios

```text
├─ core/              # Configuración principal (settings, urls, wsgi)
├─ apps/              # Carpeta contenedora de aplicaciones
│ ├─ products/        # Gestión de servicios (catalog, details)
│ ├─ orders/          # Gestión de carrito y checkout
│ ├─ users/           # Perfiles y autenticación (auth, profile)
│ └─ pages/           # Páginas estáticas (home, about, contact)
├─ static/            # Archivos CSS, JS, Imágenes globales
├─ templates/
│ ├── components/     # navbar, footer, etc.
│ ├── base.html       # Template principal
│ ├── pages/          # Templates para la app 'pages'
│ ├── users/          # Templates para la app 'users'
│ ├── products/       # Templates para la app 'products'
│ └─ orders/          # Templates para la app 'orders'
├─ .env               # Variables sensibles (DB, Secret Key)
├─ manage.py          # Gestión Django
├─ pyproject.toml     # Dependencias (uv)
├─ requirements.txt   # Dependencias (pip)
└─ README.md          # Este archivo
```

## 🛠️ Configuración y Ejecución Local

### Requisitos Previos

- **Python:** 3.11 o superior
- **PostgreSQL:** 15 o superior
- **virtualenvwrapper:** instalado y configurado
- **Git:** para clonar el repositorio

### Instalación de virtualenvwrapper (si no lo tienes)

**Windows:**
```bash
pip install virtualenvwrapper-win
```

**Linux/Mac:**
```bash
pip install virtualenvwrapper
# Agregar a ~/.bashrc o ~/.zshrc:
source /usr/local/bin/virtualenvwrapper.sh
```

### Pasos de Configuración

#### 1. Clonar el repositorio

```bash
git clone https://github.com/RACPSC2025/Eshop-Services-Smartphones.git
cd Eshop-Services-Smartphones
```

#### 2. Crear el entorno virtual

```bash
# Crear entorno virtual llamado xiaomi_shop
mkvirtualenv -p python xiaomi_shop
```

Esto automáticamente activará el entorno. Verás `(xiaomi_shop)` en tu prompt.

#### 3. Instalar dependencias

```bash
# Asegurarte de estar en el entorno
workon xiaomi_shop

# Instalar dependencias
pip install -r requirements.txt
```

#### 4. Configurar base de datos PostgreSQL

**Crea la base de datos:**

```bash
# Conectarse a PostgreSQL
psql -U postgres

# Una vez dentro, crear la base de datos
CREATE DATABASE unlockxiaomi_db;
\q
```

#### 5. Configurar variables de entorno

Crea el archivo `.env` en la raíz del proyecto:

```bash
cp .env.example .env
```

Edita el archivo `.env` con tu configuración:

```env
# Django
SECRET_KEY=django-insecure-dev-key-change-in-production

# PostgreSQL Database
POSTGRES_DB_NAME=unlockxiaomi_db
POSTGRES_DB_USER=postgres
POSTGRES_DB_PASSWORD=tu_contraseña_postgres
POSTGRES_DB_HOST=localhost
POSTGRES_DB_PORT=5432
```

**Importante:** El archivo `.env` está en `.gitignore` por seguridad. No lo subas a git.

#### 6. Ejecutar migraciones de base de datos

```bash
python manage.py migrate
```

#### 7. Descargar y construir Tailwind CSS

```bash
# Descargar Tailwind CLI
python manage.py tailwind download_cli

# Construir estilos de producción
python manage.py tailwind build
```

#### 8. Crear superusuario (opcional)

```bash
python manage.py createsuperuser
```

Sigue las instrucciones para crear email, usuario y contraseña.

#### 9. Ejecutar el servidor de desarrollo

```bash
python manage.py runserver
```

Ahora puedes acceder a:
- **Sitio web:** http://127.0.0.1:8000/
- **Panel de administración:** http://127.0.0.1:8000/admin/

#### 10. Detener el servidor

Presiona `Ctrl + C` en la terminal.

---

## 🔄 Comandos Útiles de virtualenvwrapper

```bash
# Activar entorno
workon xiaomi_shop

# Desactivar entorno
deactivate

# Ver todos los entornos virtuales
lsvirtualenv

# Eliminar un entorno
rmvirtualenv nombre_entorno
```

---

## 🚀 Despliegue en Producción

Para el despliegue en producción, utiliza:

- **Servidor WSGI:** Gunicorn (ya instalado)
  ```bash
  gunicorn --bind 0.0.0.0:8000 --workers 3 core.wsgi:application
  ```
- **Configuración de producción:**
  - `DEBUG=False`
  - `ALLOWED_HOSTS=['tudominio.com']`
  - `SECRET_KEY` seguro y único
- **Proxy inverso:** Nginx recomendado
- **SSL/TLS:** Certificado Let's Encrypt

### Variables de Entorno para Producción

Asegúrate de configurar estas variables:

- `DEBUG=False`
- `ALLOWED_HOSTS=tudominio.com,www.tudominio.com`
- `SECRET_KEY` (genera una clave segura y única)
- Credenciales de base de datos seguras

---

## 📊 Funcionalidades Implementadas

### ✅ Completado

1. **Página de Inicio Premium**
   - Hero slider de 2 slides con controles
   - Brands marquee animado (Xiaomi, Apple, Samsung, Huawei)
   - Tab switcher (Servicios/Productos)
   - Product cards con wishlist, ratings, add to cart
   - Testimonials carousel navegable
   - Trust indicators (20min servicio, 90 días garantía)

2. **Sistema de Carrito de Compras**
   - Backend robusto en Django con persistencia
   - Experiencia de usuario con JavaScript moderno
   - Soporte para usuarios e invitados
   - Mini-carrito funcional con resumen

3. **Proceso de Checkout**
   - Formulario de envío con validación
   - Proceso transaccional seguro (Atomicidad)
   - Página de confirmación con detalles del pedido

4. **Sistema de Usuarios**
   - Registro e inicio de sesión
   - Perfil de usuario con historial de pedidos
   - Panel de administración completo

5. **Navbar Sticky**
   - Logo UnlockXiaomi
   - Navegación desktop (Inicio, Servicios, Nosotros, Contacto)
   - Theme toggle (dark/light mode)
   - Shopping cart badge
   - Backdrop blur effect

6. **Sistema de Routing**
   - URLs configuradas para todas las apps
   - Named URLs ({% url 'pages:home' %})

7. **Base Template**
   - Integración Django-Tailwind CLI
   - Carga de Google Fonts
   - Material Icons
   - JavaScript modular

### 🎨 Sistema de Diseño (Tailwind 4)

#### Características de UI/UX Implementadas

✅ **Dark Mode Completo**
- Toggle con persistencia localStorage
- Transiciones suaves (duration-500)
- Iconos adaptativos (light_mode/dark_mode)

✅ **Componentes Premium**
- Glassmorphism (backdrop-blur-sm)
- Gradientes suaves (from-xiaomi to-accent)
- Sombras elevadas (shadow-xl, shadow-2xl)
- Bordes redondeados generosos (rounded-2xl, rounded-[2rem])

✅ **Micro-animaciones**
- Efectos hover (scale, translate, color)
- Animaciones de pulso (badges, indicators)
- Marquee infinito (brands strip)
- Hero slider con transiciones suaves

✅ **Diseño Responsive**
- Mobile-first
- Breakpoints: sm (40rem), md (48rem), lg (64rem), xl (80rem)
- Grid adaptativo (grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4)

---

## 🤝 Contribución

1. Haz fork del repositorio
2. Crea una rama para la funcionalidad (`git checkout -b feature/amazing-feature`)
3. Haz tus cambios
4. Confirma tus cambios (`git commit -m 'Agregue alguna funcionalidad asombrosa'`)
5. Sube a la rama (`git push origin feature/amazing-feature`)
6. Abre un Pull Request

---

## 📄 Licencia

Este proyecto está licenciado bajo la Licencia MIT - consulta el archivo LICENSE para obtener más detalles.

---

## 📋 Descripción Detallada del Proyecto

### 🎯 Resumen Ejecutivo

**UnlockXiaomi Colombia** es una plataforma e-commerce especializada en servicios técnicos certificados y venta de productos para dispositivos Xiaomi/Poco. El proyecto utiliza tecnologías de vanguardia: Django 6.0, Tailwind CSS 4.1.18, PostgreSQL y Python 3.11+.

**Estado actual:** Fundación sólida con diseño premium completo, con backend estructural implementado (modelos de e-commerce, carrito, autenticación, checkout), listo para funcionalidades avanzadas.

### 🗄️ Modelos de Datos Implementados

#### `orders.Order`
- Relación con usuario
- Estados del pedido (PENDING, PROCESSING, SHIPPED, DELIVERED, CANCELLED, REFUNDED)
- Métodos de pago (CASH, CARD, TRANSFER, MERCADOPAGO, PSE)
- Información completa de envío
- Cálculos de montos con IVA (19% Colombia)
- Timestamps y validadores

#### `orders.OrderItem`
- Relación con Order y Product
- Precio histórico (al momento de la compra)
- Cantidad con validación

#### `orders.Cart`
- Soporte para usuarios autenticados e invitados (por sesión)
- Métodos para cálculo de totales
- Timestamps de actualización

#### `orders.CartItem`
- Relación con Cart y Product
- Cantidad con validación
- Métodos para manipulación de cantidades
- Constraint único para evitar duplicados

#### `users.Profile`
- Extensión del modelo User
- Información personal y de contacto
- Dirección completa
- Avatar con ImageField
- Preferencias de usuario

### 📈 Estado de Completitud

- **Backend:** 60% completado (modelos, autenticación, carrito y checkout funcionales)
- **Frontend:** 70% completado (diseño premium implementado)
- **Infraestructura:** 80% completado (media files, configuración)
- **Admin:** 90% completado (panel funcional con vistas personalizadas)

### Funcionalidad E-commerce:
- **Modelos de datos:** ✅ 100% completado
- **Gestión admin:** ✅ 90% completado
- **Lógica de carrito:** ✅ 100% completado
- **Checkout:** ✅ 100% completado
- **Autenticación:** ✅ 100% completado

### 🔐 Seguridad

- **SECRET_KEY** en .env (no hardcodeado)
- **PostgreSQL** con credenciales en .env
- **CSRF Protection** habilitado
- Validación de formularios
- Protección contra inyección SQL (ORM Django)
- Validación de entradas de usuario

---

## 🎯 Fortalezas del Proyecto

1. ✅ **Stack ultra-moderno** (Django 6, Tailwind 4, Python 3.11+)
2. ✅ **Diseño premium** comparable a tiendas oficiales Xiaomi
3. ✅ **Arquitectura modular** y escalable
4. ✅ **Dark mode nativo** con UX pulida
5. ✅ **Backend estructural completo** para e-commerce funcional
6. ✅ **Fácil configuración local** sin Docker

---

## 📞 Recursos

- **Django Docs:** https://docs.djangoproject.com/en/6.0/
- **Tailwind CSS 4:** https://tailwindcss.com/docs
- **PostgreSQL:** https://www.postgresql.org/docs/
- **virtualenvwrapper:** https://virtualenvwrapper.readthedocs.io/

---

## 💡 Notas Importantes

- El proyecto **NO usa Docker** para desarrollo local
- Usa **virtualenvwrapper** para gestión de entornos virtuales
- El archivo `.env` contiene información sensible y **NO debe subirse** a git
- Para cambiar entre ramas: `git checkout main` o `git checkout develop`

---

## 🐛 Solución de Problemas

### El servidor no inicia

Verifica que:
1. PostgreSQL esté corriendo
2. Las credenciales en `.env` sean correctas
3. La base de datos `unlockxiaomi_db` exista
4. El entorno virtual `xiaomi_shop` esté activado

### Errores de migración

```bash
# Eliminar base de datos y volver a crear
psql -U postgres -c "DROP DATABASE unlockxiaomi_db;"
psql -U postgres -c "CREATE DATABASE unlockxiaomi_db;"

# Volver a ejecutar migraciones
python manage.py migrate
```

### Tailwind CSS no se construye

```bash
# Forzar descarga y reconstrucción
python manage.py tailwind download_cli
python manage.py tailwind build
```

---

**Desarrollado con ❤️ para la comunidad de Xiaomi en Colombia**
