<div align="center" style="background: #F75A02; padding: 20px; border-radius: 15px; margin: 10px 0;">
  <img src="static/assets/images/Mascota-Auth.png" alt="Mascota UnlockXiaomi" width="200" height="200" style="border-radius: 50%; object-fit: contain;"/>

# <span style="color: white;">UNLOCKXIAOMI - SERVICIO TÉCNICO GARANTIZADO</span>

  <p style="color: white;"><strong>Especialistas en desbloqueo, reparación y servicios técnicos certificados para dispositivos Xiaomi y Poco</strong></p>

  <div style="background: linear-gradient(135deg, #F75A02 0%, #d64a00 100%); padding: 15px; border-radius: 15px; color: white; margin: 15px 0;">
    <strong>20min</strong> Tiempo Promedio | <strong>90 días</strong> Garantía | <strong>100%</strong> Éxito | <strong>24/7</strong> Soporte
  </div>
</div>

# UnlockXiaomi Colombia - Plataforma E-commerce

**UnlockXiaomi Colombia** es una plataforma e-commerce premium especializada en servicios técnicos certificados y venta de productos para dispositivos Xiaomi, Samsung y mas.

El proyecto utiliza tecnologías de vanguardia: Django 6.0, Tailwind CSS 4.1.18, PostgreSQL 15 y Python 3.13.

## 🚀 Stack Tecnológico

### Backend

-   **Framework:** Django 6.0 (última versión)
-   **Python:** 3.13
-   **Base de datos:** PostgreSQL 15
-   **Package manager:** uv
-   **Dependencias principales:**
    -   `django-tailwind-cli==4.5.1`
    -   `gunicorn>=23.0.0`
    -   `pillow==12.1.0` (procesamiento de imágenes)
    -   `psycopg[binary]==3.3.2` (driver PostgreSQL)
    -   `python-dotenv==1.2.1`

### Frontend

-   **CSS Framework:** Tailwind CSS 4.1.18 (Motor Oxide - Rust)
-   **Fuentes:** Inter, Poppins (Google Fonts)
-   **Iconos:** Material Icons
-   **Vanilla JavaScript** para interactividad

### DevOps

-   **Containerización:** Docker + Docker Compose
-   **Base de datos:** PostgreSQL 15 container

## 📁 Arquitectura del Proyecto

### Estructura de Directorios

```text
├─ core/ # Configuración principal (settings, urls, wsgi)
├─ apps/ # Carpeta contenedora de aplicaciones
│ ├─ products/ # Gestión de servicios (catalog, details)
│ ├─ orders/ # Gestión de carrito y checkout
│ ├─ users/ # Perfiles y autenticación (auth, profile)
│ └─ pages/ # Páginas estáticas (home, about, contact)
├─ static/ # Archivos CSS, JS, Imágenes globales
├─ templates/
│ ├── components/ # navbar, footer, etc.
│ │ ├── footer.html
│ │ └── navbar.html
│ ├── base.html # Template principal (base)
│ ├── pages/ # Templates para la app 'pages'
│ │ ├── about.html
│ │ ├── contact.html
│ │ └── home.html
│ ├── users/ # Templates para la app 'users'
│ │ ├── auth.html
│ │ └── profile.html
│ ├── products/ # Templates para la app 'products'
│ │ ├── catalog.html
│ │ └── details.html
│ └── orders/ # Templates para la app 'orders'
│   ├── cart.html
│   └── checkout.html
├─ .env # Variables sensibles (DB, Secret Key)
├─ docker-compose.yml # Orquestación containers
├─ Dockerfile # Imagen Django
├─ .dockerignore # Archivo para excluir archivos del contexto de Docker
├─ manage.py
├─ pyproject.toml # Dependencias (uv)
└─ uv.lock
```

## 🐳 Configuración y Ejecución con Docker

### Requisitos previos

-   Docker Engine (20.10 o superior)
-   Docker Compose (v2 o superior)
-   Git

### Configuración de docker-compose.yml

Los archivos `docker-compose.yml` (producción) y `docker-compose.dev.yml` (desarrollo) están configurados con:

-   **Versión:** 3.8 de Docker Compose
-   **Servicio web:**
    -   Construcción desde el Dockerfile local
    -   Comando producción: `gunicorn --bind 0.0.0.0:8000 --workers 3 core.wsgi:application`
    -   Comando desarrollo: `python manage.py runserver 0.0.0.0:8000`
    -   Volumen: Montaje del directorio local para desarrollo
    -   Puerto: 8000 expuesto
    -   Dependencia: Requiere el servicio 'db'
    -   Variables de entorno: Cargadas desde .env
-   **Servicio db:**
    -   Imagen: PostgreSQL 15
    -   Volumen: Persistente para mantener datos
    -   Variables de entorno: Configuración de PostgreSQL
-   **Volumen:** `postgres_data` para persistencia de datos

### Ejecución con Docker

#### 1. Clonar el repositorio

```bash
git clone <repository-url>
cd UnlockXiaomi
```

#### 2. Configurar variables de entorno

Cree un archivo `.env` basado en `.env.example`:

```bash
cp .env.example .env
```

Edite el archivo `.env` con su configuración específica:

```env
SECRET_KEY=your-secret-key-here
POSTGRES_DB_NAME=your_db_name
POSTGRES_DB_USER=your_db_user
POSTGRES_DB_PASSWORD=your_db_password
POSTGRES_DB_HOST=db
POSTGRES_DB_PORT=5432
```

#### 3. Construir y ejecutar con Docker Compose (Recomendado)

```bash
# Construir e iniciar todos los servicios (modo detached)
docker-compose up --build

# O ejecutar en primer plano para ver los logs
docker-compose up
```

#### 4. Modo Desarrollo vs Producción

Por defecto, `docker-compose.yml` usa Gunicorn para producción. Para desarrollo con recarga automática:

-   Modifique el comando en `docker-compose.yml` a: `python manage.py runserver 0.0.0.0:8000`
-   O use el archivo `docker-compose.dev.yml` adicional para desarrollo:

```bash
# Ejecutar en modo desarrollo
docker-compose -f docker-compose.dev.yml up --build
```

#### 5. Alternativa: Construir y ejecutar Dockerfile directamente

```bash
# Construir la imagen
docker build -t unlockxiaomi .

# Ejecutar el contenedor (después de configurar PostgreSQL por separado)
docker run -p 8000:8000 --env-file .env unlockxiaomi
```

### Archivo .dockerignore

El archivo `.dockerignore` excluye archivos innecesarios del contexto de construcción de Docker, incluyendo:

-   Archivos de Python (**pycache**, \*.pyc, etc.)
-   Entornos virtuales (.venv/, env/, etc.)
-   Archivos de Django (media/, staticfiles/, \*.log, etc.)
-   Archivos de IDE (.vscode/, .idea/, etc.)
-   Archivos de sistema (.git/, .DS_Store, Thumbs.db, etc.)
-   Otros archivos innecesarios para la construcción de la imagen

### Consideraciones para Producción con Docker

Para despliegue en producción, considere:

-   Usar un servidor WSGI como Gunicorn en lugar de runserver
-   Configurar variables de entorno específicas para producción
-   Usar un volumen externo para archivos media
-   Configurar un proxy inverso como Nginx
-   Implementar SSL/TLS para conexiones seguras

### Configuración de la base de datos

La primera vez que ejecute la aplicación, necesitará ejecutar las migraciones:

```bash
# Si ejecuta con docker-compose, ejecute en el contenedor web:
docker-compose exec web python manage.py migrate

# Si ejecuta el contenedor directamente:
docker exec -it <container-id> python manage.py migrate
```

### Creación de un superusuario

Para crear un usuario administrador para el panel de Django:

```bash
# Con docker-compose:
docker-compose exec web python manage.py createsuperuser

# Con contenedor directo:
docker exec -it <container-id> python manage.py createsuperuser
```

## 🛠️ Configuración de Desarrollo Local

Si prefiere ejecutar la aplicación localmente sin Docker:

### 1. Requisitos del sistema

-   Python 3.13
-   PostgreSQL 15
-   Node.js (para Tailwind CLI, si se necesita localmente)

### 2. Pasos de configuración

```bash
# 1. Clonar y navegar al proyecto
cd UnlockXiaomi

# 2. Crear entorno virtual
python -m venv .venv
source .venv/bin/activate  # Linux/Mac: .venv/bin/activate
# Windows: .venv\Scripts\activate

# 3. Instalar dependencias
pip install uv
uv pip install -p pyproject.toml

# 4. Configurar entorno
cp .env.example .env
# Editar .env con sus credenciales de base de datos

# 5. Ejecutar migraciones de base de datos
python manage.py migrate

# 6. Descargar y construir Tailwind CSS
python manage.py tailwind download_cli
python manage.py tailwind build

# 7. Recopilar archivos estáticos
python manage.py collectstatic --noinput

# 8. Crear superusuario (opcional)
python manage.py createsuperuser

# 9. Ejecutar el servidor de desarrollo
python manage.py runserver
```

## 🚀 Despliegue en Producción

Para el despliegue en producción, la imagen Docker está configurada con:

-   Servidor WSGI Gunicorn con 3 workers
-   Configuración de producción (DEBUG=False)
-   Usuario no root para seguridad
-   Manejo adecuado de archivos estáticos

### Variables de entorno para Producción

Asegúrese de que estas variables de entorno estén configuradas en producción:

-   `DEBUG=False`
-   `ALLOWED_HOSTS=yourdomain.com`
-   `SECRET_KEY` segura
-   Credenciales de base de datos adecuadas

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

    - Logo MiXiaomiUnlock
    - Navegación desktop (Inicio, Servicios, Nosotros, Contacto)
    - Theme toggle
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

-   Toggle con persistencia localStorage
-   Transiciones suaves (duration-500)
-   Iconos adaptativos (light_mode/dark_mode)

✅ **Componentes Premium**

-   Glassmorphism (backdrop-blur-sm)
-   Gradientes suaves (from-xiaomi to-accent)
-   Sombras elevadas (shadow-xl, shadow-2xl)
-   Bordes redondeados generosos (rounded-2xl, rounded-[2rem])

✅ **Micro-animaciones**

-   Efectos hover (scale, translate, color)
-   Animaciones de pulso (badges, indicators)
-   Marquee infinito (brands strip)
-   Hero slider con transiciones suaves

✅ **Diseño Responsive**

-   Mobile-first
-   Breakpoints: sm (40rem), md (48rem), lg (64rem), xl (80rem)
-   Grid adaptativo (grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4)

## 🤝 Contribución

1. Haga un fork del repositorio
2. Cree una rama para la funcionalidad (`git checkout -b feature/amazing-feature`)
3. Haga sus cambios
4. Confirme sus cambios (`git commit -m 'Agregue alguna funcionalidad asombrosa'`)
5. Suba a la rama (`git push origin feature/amazing-feature`)
6. Abra un Pull Request

## 📄 Licencia

Este proyecto está licenciado bajo la Licencia MIT - consulte el archivo LICENSE para obtener más detalles.

---

## 📋 Descripción Detallada del Proyecto

### 🎯 Resumen Ejecutivo

**UnlockXiaomi Colombia** es una plataforma e-commerce especializada en servicios técnicos certificados y venta de productos para dispositivos Xiaomi/Poco. El proyecto utiliza tecnologías de vanguardia: Django 6.0, Tailwind CSS 4.1.18, PostgreSQL 15, y Python 3.13.

**Estado actual:** Fundación sólida con diseño premium completo, con backend estructural implementado (modelos de e-commerce, carrito, autenticación, checkout), listo para funcionalidades avanzadas.

### 🚀 Características Principales Implementadas

#### 1. **Home Page Premium**

-   Hero slider de 2 slides con controles y transiciones suaves
-   Brands marquee animado (Xiaomi, Apple, Samsung, Huawei)
-   Tab switcher (Servicios/Productos) con "Servicios" como pestaña predeterminada
-   Product cards con wishlist, ratings, add to cart
-   Testimonials carousel navegable con controles
-   Trust indicators (20min servicio, 90 días garantía)
-   **Nueva Sección Bento Grid** con información educativa sobre problemas comunes de smartphones y soluciones
-   Separadores con gradientes para mejor experiencia visual

#### 2. **Sistema de Carrito de Compras**

-   Backend robusto en Django con persistencia
-   Experiencia de usuario con JavaScript moderno
-   Soporte para usuarios e invitados
-   Mini-carrito funcional con resumen
-   Integración completa con AJAX para actualizaciones en tiempo real
-   Botones de "Agregar al Carrito" con feedback visual

#### 3. **Proceso de Checkout**

-   Formulario de envío con validación
-   Proceso transaccional seguro (Atomicidad)
-   Página de confirmación con detalles del pedido
-   Cálculo automático de totales e IVA (19% Colombia)

#### 4. **Sistema de Usuarios**

-   Registro e inicio de sesión
-   Perfil de usuario con historial de pedidos
-   Panel de administración completo
-   Soporte para perfiles extendidos con información personal y direcciones

#### 5. **Catálogo de Productos**

-   Vista de catálogo con paginación
-   Filtros por servicios y productos
-   Vista detallada de productos
-   Integración con imágenes estáticas
-   Vista de productos organizada en grid responsive

#### 6. **Sistema de Diseño (Tailwind 4)**

-   Dark Mode Completo con toggle persistente
-   Componentes Premium con glassmorphism y gradientes
-   Micro-animaciones y transiciones suaves
-   Diseño completamente responsive
-   Bento Grid layout para contenido educativo
-   Efectos hover y animaciones avanzadas

### 🗄️ Modelos de Datos Implementados

#### `orders.Order`

-   Relación con usuario
-   Estados del pedido (PENDING, PROCESSING, SHIPPED, DELIVERED, CANCELLED, REFUNDED)
-   Métodos de pago (CASH, CARD, TRANSFER, MERCADOPAGO, PSE)
-   Información completa de envío
-   Cálculos de montos con IVA (19% Colombia)
-   Timestamps y validadores

#### `orders.OrderItem`

-   Relación con Order y Product
-   Precio histórico (al momento de la compra)
-   Cantidad con validación

#### `orders.Cart`

-   Soporte para usuarios autenticados e invitados (por sesión)
-   Métodos para cálculo de totales
-   Timestamps de actualización

#### `orders.CartItem`

-   Relación con Cart y Product
-   Cantidad con validación
-   Métodos para manipulación de cantidades
-   Constraint único para evitar duplicados

#### `users.Profile`

-   Extensión del modelo User
-   Información personal y de contacto
-   Dirección completa
-   Avatar con ImageField
-   Preferencias de usuario

### 🎨 Características de UI/UX Implementadas

✅ **Dark Mode Completo**

-   Toggle con persistencia localStorage
-   Transiciones suaves (duration-500)
-   Iconos adaptativos (light_mode/dark_mode)

✅ **Componentes Premium**

-   Glassmorphism (backdrop-blur-sm)
-   Gradientes suaves (from-xiaomi to-accent)
-   Sombras elevadas (shadow-xl, shadow-2xl)
-   Bordes redondeados generosos (rounded-2xl, rounded-[2rem])

✅ **Micro-animaciones**

-   Efectos hover (scale, translate, color)
-   Animaciones de pulso (badges, indicators)
-   Marquee infinito (brands strip)
-   Hero slider con transiciones suaves
-   Bento Grid con interacción dinámica

✅ **Diseño Responsive**

-   Mobile-first
-   Breakpoints: sm (40rem), md (48rem), lg (64rem), xl (80rem)
-   Grid adaptativo (grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4)
-   Layouts avanzados con Bento Grid (auto-rows, grid-span)

### 📈 Estado de Completitud

-   **Backend:** 60% completado (modelos, autenticación, carrito y checkout funcionales)
-   **Frontend:** 70% completado (diseño premium implementado)
-   **Infraestructura:** 80% completado (Docker, CI/CD, media files)
-   **Admin:** 90% completado (panel funcional con vistas personalizadas)

### Funcionalidad E-commerce:

-   **Modelos de datos:** ✅ 100% completado
-   **Gestión admin:** ✅ 90% completado
-   **Lógica de carrito:** ✅ 100% completado
-   **Checkout:** ✅ 100% completado
-   **Autenticación:** ✅ 100% completado

### 🔐 Seguridad

-   **SECRET_KEY** en .env (no hardcodeado)
-   **PostgreSQL** con credenciales en .env
-   **CSRF Protection** habilitado
-   Validación de formularios
-   Protección contra inyección SQL (ORM Django)
-   Validación de entradas de usuario

### 📊 Tecnologías Relevantes

#### Django 6.0 Features

-   Model Fields en Enums (TextChoices)
-   Async ORM Queries
-   PostgreSQL Connection Pooling
-   LoginRequiredMiddleware

#### Tailwind CSS 4.0+

-   Motor Oxide (Rust) - builds más rápidos
-   CSS-First Configuration con @theme
-   Auto Source Detection
-   Nuevas utilidades disponibles

### 📈 Roadmap Actualizado

#### Fase 1: MVP Funcional (Completada)

-   ✅ Implementar modelos de Order/Cart
-   ✅ Sistema de carrito funcional
-   ✅ Autenticación básica (login/register)
-   ✅ Checkout simple
-   ✅ Admin panel configurado
-   ✅ Catálogo dinámico con pagination

#### Fase 2: E-commerce Completo (Completada)

-   ✅ Integración de pasarela de pago
-   ✅ Sistema de emails
-   ✅ Página de detalles de producto
-   ✅ User profile completo
-   ✅ Order history
-   ✅ Gestión de media files

#### Fase 3: Optimización (En progreso)

-   ⚡ SEO optimization
-   ⚡ Performance tuning
-   ⚡ Testing completo
-   ⚡ Deployment a staging
-   ⚡ Security audit

#### Fase 4: Features Avanzadas (Por implementar)

-   🔄 Reviews y ratings
-   🔄 Wishlist
-   🔄 Recommendations
-   🔄 Analytics dashboard
-   🔄 Marketing (newsletter, promos)

### 🎯 Nueva Funcionalidad: Bento Grid Educativo

#### Sección de Educación del Usuario

-   **Bento Grid Layout:** Diseño avanzado con layout de cuadrícula asimétrica
-   **Contenido Interactivo:** Clic en tarjetas pequeñas intercambia contenido con la tarjeta principal
-   **Educación del Usuario:** Información sobre problemas comunes de smartphones (IMEI, Google Cloud, Mi Cloud, Bootloader)
-   **Experiencia Visual:** Transiciones suaves y efectos hover en todas las tarjetas
-   **Contenido Dinámico:** Integración con productos reales del catálogo para mostrar ejemplos

### 🎯 Fortalezas del Proyecto

1. ✅ **Stack ultra-moderno** (Django 6, Tailwind 4, Python 3.13)
2. ✅ **Diseño premium** comparable a tiendas oficiales Xiaomi
3. ✅ **Arquitectura modular** y escalable
4. ✅ **Dark mode nativo** con UX pulida
5. ✅ **Docker-ready** para deployment consistente
6. ✅ **Backend estructural completo** para e-commerce funcional

### 📞 Recursos

-   **Django Docs:** https://docs.djangoproject.com/en/6.0/
-   **Tailwind CSS 4:** https://tailwindcss.com/docs
-   **PostgreSQL:** https://www.postgresql.org/docs/
-   **MercadoPago SDK:** https://www.mercadopago.com.co/developers
