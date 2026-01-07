from decimal import Decimal
from typing import TYPE_CHECKING

from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from django.db import models
from django.db.models import Manager, QuerySet

from apps.products.models import Product

if TYPE_CHECKING:
    from .models import OrderItem, CartItem  # Evita import circular


class Order(models.Model):
    """Modelo para gestionar pedidos/órdenes de compra"""

    class OrderStatus(models.TextChoices):
        PENDING = "PENDING", "Pendiente"
        PROCESSING = "PROCESSING", "Procesando"
        SHIPPED = "SHIPPED", "Enviado"
        DELIVERED = "DELIVERED", "Entregado"
        CANCELLED = "CANCELLED", "Cancelado"
        REFUNDED = "REFUNDED", "Reembolsado"

    class PaymentMethod(models.TextChoices):
        CASH = "CASH", "Efectivo"
        CARD = "CARD", "Tarjeta"
        TRANSFER = "TRANSFER", "Transferencia"
        MERCADOPAGO = "MERCADOPAGO", "MercadoPago"
        PSE = "PSE", "PSE"

    # Relaciones
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="orders",
        verbose_name="Usuario",
    )

    # Información de envío
    shipping_name = models.CharField("Nombre completo", max_length=200)
    shipping_email = models.EmailField("Email")
    shipping_phone = models.CharField("Teléfono", max_length=20)
    shipping_address = models.TextField("Dirección")
    shipping_city = models.CharField("Ciudad", max_length=100)
    shipping_department = models.CharField("Departamento", max_length=100, blank=True)
    shipping_postal_code = models.CharField("Código postal", max_length=10, blank=True)

    # Información de pago
    payment_method = models.CharField(
        "Método de pago",
        max_length=20,
        choices=PaymentMethod.choices,
        default=PaymentMethod.CASH,
    )
    payment_status = models.BooleanField("Pago confirmado", default=False)
    transaction_id = models.CharField("ID de transacción", max_length=200, blank=True)

    # Estado y montos
    status = models.CharField(
        "Estado",
        max_length=20,
        choices=OrderStatus.choices,
        default=OrderStatus.PENDING,
    )

    subtotal = models.DecimalField(
        "Subtotal",
        max_digits=12,
        decimal_places=2,
        default=Decimal("0.00"),
        validators=[MinValueValidator(Decimal("0.00"))],
    )
    tax = models.DecimalField(
        "IVA (19%)",
        max_digits=12,
        decimal_places=2,
        default=Decimal("0.00"),
        validators=[MinValueValidator(Decimal("0.00"))],
    )
    shipping_cost = models.DecimalField(
        "Costo de envío",
        max_digits=12,
        decimal_places=2,
        default=Decimal("0.00"),
        validators=[MinValueValidator(Decimal("0.00"))],
    )
    discount = models.DecimalField(
        "Descuento",
        max_digits=12,
        decimal_places=2,
        default=Decimal("0.00"),
        validators=[MinValueValidator(Decimal("0.00"))],
    )
    total = models.DecimalField(
        "Total",
        max_digits=12,
        decimal_places=2,
        default=Decimal("0.00"),
        validators=[MinValueValidator(Decimal("0.00"))],
    )

    # Notas
    notes = models.TextField("Notas del pedido", blank=True)
    admin_notes = models.TextField("Notas internas", blank=True)

    # Timestamps
    created_at = models.DateTimeField("Fecha de creación", auto_now_add=True)
    updated_at = models.DateTimeField("Última actualización", auto_now=True)

    # Type hints para evitar errores de tipado
    if TYPE_CHECKING:
        id: int
        items: Manager["OrderItem"]

        def get_status_display(self) -> str: ...

    class Meta:
        verbose_name = "Pedido"
        verbose_name_plural = "Pedidos"
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["-created_at"]),
            models.Index(fields=["user", "status"]),
        ]

    def __str__(self) -> str:
        return f"Pedido #{self.id} - {self.user.username} - {self.get_status_display()}"

    def calculate_totals(self) -> None:
        """Calcula y actualiza subtotal, tax, total basado en los items"""
        items = self.items.all()
        self.subtotal = sum((item.get_total_price() for item in items), start=Decimal("0.00"))
        self.tax = Decimal("0.00")  # IVA deshabilitado
        self.total = self.subtotal + self.tax + self.shipping_cost - self.discount
        self.save(update_fields=["subtotal", "tax", "total"])

    def get_items_count(self) -> int:
        """Retorna la cantidad total de productos (suma de cantidades)"""
        return sum(item.quantity for item in self.items.all())


class OrderItem(models.Model):
    """Items individuales de un pedido"""

    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name="items",
        verbose_name="Pedido",
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.PROTECT,
        related_name="order_items",
        verbose_name="Producto",
    )
    quantity = models.PositiveIntegerField(
        "Cantidad",
        default=1,
        validators=[MinValueValidator(1)],
    )
    price = models.DecimalField(
        "Precio unitario al momento de la compra",
        max_digits=10,
        decimal_places=2,
    )

    created_at = models.DateTimeField("Fecha de agregado", auto_now_add=True)

    class Meta:
        verbose_name = "Item de pedido"
        verbose_name_plural = "Items de pedido"
        ordering = ["id"]

    def __str__(self) -> str:
        return f"{self.quantity}x {self.product.name} en Pedido #{self.order.id}"

    def get_total_price(self) -> Decimal:
        """Precio total de este ítem"""
        return self.price * Decimal(self.quantity)


class Cart(models.Model):
    """Carrito de compras (autenticado o de sesión)"""

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="cart",
        verbose_name="Usuario",
        null=True,
        blank=True,
        help_text="Null para carritos de invitados",
    )
    session_key = models.CharField(
        "Clave de sesión",
        max_length=40,
        blank=True,
        help_text="Para usuarios no autenticados",
    )
    created_at = models.DateTimeField("Fecha de creación", auto_now_add=True)
    updated_at = models.DateTimeField("Última actualización", auto_now=True)

    if TYPE_CHECKING:
        items: Manager["CartItem"]

    class Meta:
        verbose_name = "Carrito"
        verbose_name_plural = "Carritos"
        ordering = ["-updated_at"]

    def __str__(self) -> str:
        if self.user:
            return f"Carrito de {self.user.username}"
        return f"Carrito invitado ({self.session_key[:8]}...)"

    def get_total_items(self) -> int:
        """Cantidad total de productos (suma de cantidades)"""
        return sum(item.quantity for item in self.items.all())

    def get_subtotal(self) -> Decimal:
        """Subtotal sin impuestos ni envío"""
        return sum((item.get_total_price() for item in self.items.all()), start=Decimal("0.00"))

    def get_tax(self) -> Decimal:
        """IVA 19% sobre el subtotal"""
        return Decimal("0.00") # IVA deshabilitado temporalmente

    def get_total(self) -> Decimal:
        """Total con IVA (sin envío ni descuento)"""
        return self.get_subtotal() + self.get_tax()

    def clear(self) -> None:
        """Elimina todos los items del carrito"""
        self.items.all().delete()


class CartItem(models.Model):
    """Items individuales del carrito"""

    cart = models.ForeignKey(
        Cart,
        on_delete=models.CASCADE,
        related_name="items",
        verbose_name="Carrito",
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="cart_items",
        verbose_name="Producto",
    )
    quantity = models.PositiveIntegerField(
        "Cantidad",
        default=1,
        validators=[MinValueValidator(1)],
    )
    added_at = models.DateTimeField("Fecha de agregado", auto_now_add=True)
    updated_at = models.DateTimeField("Última actualización", auto_now=True)

    class Meta:
        verbose_name = "Item del carrito"
        verbose_name_plural = "Items del carrito"
        unique_together = ["cart", "product"]
        ordering = ["-added_at"]

    def __str__(self) -> str:
        return f"{self.quantity}x {self.product.name}"

    def get_total_price(self) -> Decimal:
        """Precio total de este ítem en el carrito"""
        return self.product.price * Decimal(self.quantity)

    def increase_quantity(self, amount: int = 1) -> None:
        """Aumenta la cantidad del producto"""
        self.quantity += amount
        self.save(update_fields=["quantity", "updated_at"])

    def decrease_quantity(self, amount: int = 1) -> None:
        """Disminuye cantidad, elimina si llega a 0 o menos"""
        if self.quantity > amount:
            self.quantity -= amount
            self.save(update_fields=["quantity", "updated_at"])
        else:
            self.delete()
