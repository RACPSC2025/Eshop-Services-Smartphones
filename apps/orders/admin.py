from django.contrib import admin
from .models import Order, OrderItem, Cart, CartItem


class OrderItemInline(admin.TabularInline):
    """Inline para mostrar items dentro del pedido"""
    model = OrderItem
    extra = 0
    readonly_fields = ['get_total_price']
    fields = ['product', 'quantity', 'price', 'get_total_price']
    
    def get_total_price(self, obj):
        if obj.pk:
            return f"${obj.get_total_price():.2f}"
        return "-"
    get_total_price.short_description = 'Total'


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = [
        'id', 'user', 'status', 'payment_status', 'total', 
        'created_at', 'get_items_count'
    ]
    list_filter = ['status', 'payment_status', 'payment_method', 'created_at']
    search_fields = [
        'id', 'user__username', 'user__email', 
        'shipping_name', 'shipping_email', 'transaction_id'
    ]
    readonly_fields = ['created_at', 'updated_at']
    inlines = [OrderItemInline]
    
    fieldsets = (
        ('Información del Pedido', {
            'fields': ('user', 'status', 'created_at', 'updated_at')
        }),
        ('Información de Envío', {
            'fields': (
                'shipping_name', 'shipping_email', 'shipping_phone',
                'shipping_address', 'shipping_city', 'shipping_department',
                'shipping_postal_code'
            )
        }),
        ('Información de Pago', {
            'fields': (
                'payment_method', 'payment_status', 'transaction_id'
            )
        }),
        ('Montos', {
            'fields': (
                'subtotal', 'tax', 'shipping_cost', 'discount', 'total'
            )
        }),
        ('Notas', {
            'fields': ('notes', 'admin_notes'),
            'classes': ('collapse',)
        }),
    )
    
    def get_items_count(self, obj):
        return obj.get_items_count()
    get_items_count.short_description = 'Items'
    
    actions = ['mark_as_processing', 'mark_as_shipped', 'mark_as_delivered']
    
    def mark_as_processing(self, request, queryset):
        queryset.update(status=Order.OrderStatus.PROCESSING)
    mark_as_processing.short_description = "Marcar como Procesando"
    
    def mark_as_shipped(self, request, queryset):
        queryset.update(status=Order.OrderStatus.SHIPPED)
    mark_as_shipped.short_description = "Marcar como Enviado"
    
    def mark_as_delivered(self, request, queryset):
        queryset.update(status=Order.OrderStatus.DELIVERED)
    mark_as_delivered.short_description = "Marcar como Entregado"


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['id', 'order', 'product', 'quantity', 'price', 'get_total']
    list_filter = ['order__status', 'created_at']
    search_fields = ['order__id', 'product__name']
    
    def get_total(self, obj):
        return f"${obj.get_total_price():.2f}"
    get_total.short_description = 'Total'


class CartItemInline(admin.TabularInline):
    """Inline para mostrar items dentro del carrito"""
    model = CartItem
    extra = 0
    readonly_fields = ['get_total_price']
    
    def get_total_price(self, obj):
        if obj.pk:
            return f"${obj.get_total_price():.2f}"
        return "-"
    get_total_price.short_description = 'Total'


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = [
        'id', 'get_owner', 'get_total_items', 'get_total', 
        'created_at', 'updated_at'
    ]
    list_filter = ['created_at', 'updated_at']
    search_fields = ['user__username', 'session_key']
    readonly_fields = ['created_at', 'updated_at']
    inlines = [CartItemInline]
    
    def get_owner(self, obj):
        if obj.user:
            return obj.user.username
        return f"Invitado ({obj.session_key[:8]}...)"
    get_owner.short_description = 'Usuario'
    
    def get_total(self, obj):
        return f"${obj.get_total():.2f}"
    get_total.short_description = 'Total'


@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ['id', 'cart', 'product', 'quantity', 'get_total', 'added_at']
    list_filter = ['added_at']
    search_fields = ['cart__user__username', 'product__name']
    
    def get_total(self, obj):
        return f"${obj.get_total_price():.2f}"
    get_total.short_description = 'Total'

