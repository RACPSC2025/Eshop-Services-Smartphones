# ✅ Modelos Completados - UnlockXiaomi

**Fecha:** 2026-01-05  
**Estado:** Implementación exitosa

---

## 📦 Modelos Implementados

### 1. **orders.Order** ✅
Modelo principal para gestionar pedidos de compra.

**Características:**
- ✅ Relación con User (ForeignKey)
- ✅ Información de envío completa (nombre, email, teléfono, dirección, ciudad, departamento)
- ✅ Métodos de pago (Efectivo, Tarjeta, Transferencia, MercadoPago, PSE)
- ✅ Estados del pedido (Pendiente, Procesando, Enviado, Entregado, Cancelado, Reembolsado)
- ✅ Cálculos automáticos (subtotal, IVA 19%, shipping, descuento, total)
- ✅ Tracking de pago (payment_status, transaction_id)
- ✅ Notas del pedido y notas internas
- ✅ Timestamps (created_at, updated_at)
- ✅ Índices en base de datos para performance

**Métodos útiles:**
```python
order.calculate_totals()  # Calcula automáticamente totales
order.get_items_count()   # Cantidad total de items
```

---

### 2. **orders.OrderItem** ✅
Items individuales dentro de un pedido.

**Características:**
- ✅ Relación con Order (CASCADE) y Product (PROTECT)
- ✅ Quantity validator (mínimo 1)
- ✅ Precio guardado al momento de compra (no cambia si el producto sube de precio)
- ✅ Timestamp de agregado

**Métodos útiles:**
```python
item.get_total_price()  # precio * cantidad
```

---

### 3. **orders.Cart** ✅
Carrito de compras persistente.

**Características:**
- ✅ Soporte para usuarios autenticados (OneToOneField con User)
- ✅ Soporte para invitados (session_key)
- ✅ Timestamps de creación y actualización
- ✅ Relación uno-a-uno con User

**Métodos útiles:**
```python
cart.get_total_items()   # Total de items en el carrito
cart.get_subtotal()      # Subtotal sin IVA
cart.get_tax()           # IVA (19%)
cart.get_total()         # Total con IVA
cart.clear()             # Vaciar carrito
```

---

### 4. **orders.CartItem** ✅
Items individuales del carrito.

**Características:**
- ✅ Relación con Cart y Product
- ✅ Constraint UNIQUE (cart, product) - un producto solo aparece una vez
- ✅ Quantity con validación (mínimo 1)
- ✅ Timestamps

**Métodos útiles:**
```python
item.get_total_price()       # product.price * quantity
item.increase_quantity(2)    # Incrementar cantidad
item.decrease_quantity(1)    # Decrementar (elimina si llega a 0)
```

---

### 5. **users.Profile** ✅
Perfil extendido del usuario.

**Características:**
- ✅ OneToOneField con User (creación automática con signals)
- ✅ Información personal (teléfono, documento, fecha nacimiento)
- ✅ Dirección completa (dirección, ciudad, departamento, código postal, país)
- ✅ Avatar (ImageField)
- ✅ Preferencias (newsletter, email notifications)
- ✅ Auto-creación con signals cuando se crea un User

**Métodos útiles:**
```python
profile.get_full_name()              # Nombre completo del usuario
profile.has_complete_shipping_info() # Verifica info de envío
```

**Signals implementados:**
```python
@receiver(post_save, sender=User)
def create_user_profile(...)  # Crea Profile automáticamente
```

---

## 🎨 Admin Personalizado

### OrderAdmin
- ✅ Inline de OrderItems (ver items dentro del pedido)
- ✅ Filtros: status, payment_status, payment_method, created_at
- ✅ Búsqueda: id, username, email, shipping_name, transaction_id
- ✅ Fieldsets organizados (Info Pedido, Envío, Pago, Montos, Notas)
- ✅ Actions: marcar como procesando/enviado/entregado

### CartAdmin
- ✅ Inline de CartItems
- ✅ Display de totales calculados
- ✅ Identificación de usuario o invitado

### ProfileAdmin + UserAdmin Extended
- ✅ Profile como inline en UserAdmin
- ✅ Todos los campos editables desde admin
- ✅ UserAdmin re-registrado con Profile incluido

---

## 🗄️ Configuraciones Agregadas

### settings.py
```python
# Media files (User uploads - Images)
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
```

### core/urls.py
```python
from django.conf import settings
from django.conf.urls.static import static

# Servir archivos media en desarrollo
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
```

---

## ✅ Migraciones Aplicadas

```bash
✅ python manage.py makemigrations
   - Migrations for 'orders': 0001_initial
   - Migrations for 'users': 0001_initial

✅ python manage.py migrate
   - Applied successfully
```

---

## 📊 Estructura de Base de Datos

### Tablas Creadas:

**orders_order:**
- Campos: 20+ (user_id, shipping_*, payment_*, status, montos, timestamps)
- Índices: created_at, (user, status)
- Relaciones: User (FK)

**orders_orderitem:**
- Campos: order_id, product_id, quantity, price, created_at
- Relaciones: Order (CASCADE), Product (PROTECT)

**orders_cart:**
- Campos: user_id, session_key, created_at, updated_at
- Relaciones: User (OneToOne, nullable)

**orders_cartitem:**
- Campos: cart_id, product_id, quantity, added_at, updated_at
- Constraint UNIQUE: (cart, product)
- Relaciones: Cart (CASCADE), Product (CASCADE)

**users_profile:**
- Campos: user_id, phone, document_*, address_*, avatar, preferences, timestamps
- Relaciones: User (OneToOne)

---

## 🎯 Próximos Pasos Recomendados

### Alta Prioridad:
1. **Vistas de Carrito** - Implementar lógica de añadir/remover del carrito
2. **Vistas de Checkout** - Proceso de creación de Order desde Cart
3. **Autenticación** - Login/Register forms
4. **Context Processor** - Para mostrar cantidad de items en navbar

### Media Prioridad:
5. **Signals adicionales** - Para crear Order number automático
6. **Email notifications** - Confirmación de orden
7. **Stock management** - Verificar disponibilidad antes de comprar
8. **Payment gateway** - Integrar MercadoPago/PSE

---

## 💡 Ejemplos de Uso

### Crear un Pedido:
```python
from apps.orders.models import Order, OrderItem
from apps.products.models import Product
from django.contrib.auth.models import User

# Crear pedido
order = Order.objects.create(
    user=request.user,
    shipping_name="Juan Pérez",
    shipping_email="juan@example.com",
    shipping_phone="3001234567",
    shipping_address="Calle 123 #45-67",
    shipping_city="Bogotá",
    payment_method=Order.PaymentMethod.MERCADOPAGO
)

# Agregar items
product = Product.objects.get(id=1)
OrderItem.objects.create(
    order=order,
    product=product,
    quantity=2,
    price=product.price
)

# Calcular totales
order.calculate_totals()
```

### Trabajar con el Carrito:
```python
from apps.orders.models import Cart, CartItem

# Obtener o crear carrito del usuario
cart, created = Cart.objects.get_or_create(user=request.user)

# Agregar producto
product = Product.objects.get(id=1)
cart_item, created = CartItem.objects.get_or_create(
    cart=cart,
    product=product,
    defaults={'quantity': 1}
)

if not created:
    cart_item.increase_quantity()

# Ver totales
print(f"Subtotal: ${cart.get_subtotal()}")
print(f"IVA: ${cart.get_tax()}")
print(f"Total: ${cart.get_total()}")
```

### Perfil de Usuario:
```python
# El perfil se crea automáticamente
user = User.objects.create_user('nuevo_usuario', 'email@test.com', 'password')

# Actualizar perfil
profile = user.profile
profile.phone = "3001234567"
profile.address = "Calle 123"
profile.city = "Medellín"
profile.save()

# Verificar info completa
if profile.has_complete_shipping_info():
    print("Usuario puede hacer checkout")
```

---

## 🔍 Testing en Admin

Para verificar que todo funciona:

1. **Acceder al admin:** http://localhost:8000/admin/
2. **Crear superuser:**
   ```bash
   python manage.py createsuperuser
   ```
3. **Verificar secciones:**
   - ✅ Orders → Orders (ver inline de items)
   - ✅ Orders → Carts (ver inline de cart items)
   - ✅ Users → Profiles
   - ✅ Auth → Users (ver inline de Profile)
   - ✅ Products → Products

---

## 📝 Notas Importantes

- ✅ IVA configurado al 19% (Colombia)
- ✅ Archivos media se guardarán en `/media/products/` y `/media/avatars/`
- ✅ Unique constraint en CartItem evita duplicados
- ✅ PROTECT en OrderItem.product evita borrar productos con órdenes
- ✅ CASCADE en relaciones Cart/Order elimina items automáticamente
- ✅ Signals crean Profile automáticamente para nuevos usuarios

---

**Estado Final:** ✅ COMPLETADO  
**Modelos funcionando:** 5/5  
**Admin configurado:** ✅  
**Migraciones aplicadas:** ✅  
**Media files configurados:** ✅
