from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from .models import Profile


class ProfileInline(admin.StackedInline):
    """Inline para mostrar Profile dentro de User"""
    model = Profile
    can_delete = False
    verbose_name = 'Perfil'
    verbose_name_plural = 'Perfil'
    fk_name = 'user'
    fields = [
        'phone', 'document_type', 'document_number', 'birth_date',
        'address', 'city', 'department', 'postal_code', 'country',
        'avatar', 'newsletter_subscription', 'email_notifications'
    ]


class UserAdmin(BaseUserAdmin):
    """Extend UserAdmin para incluir Profile inline"""
    inlines = [ProfileInline]
    list_display = [
        'username', 'email', 'first_name', 'last_name', 
        'is_staff', 'date_joined'
    ]


# Re-registrar UserAdmin con Profile inline
admin.site.unregister(User)
admin.site.register(User, UserAdmin)


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = [
        'user', 'phone', 'city', 'newsletter_subscription', 
        'created_at'
    ]
    list_filter = ['newsletter_subscription', 'email_notifications', 'country', 'created_at']
    search_fields = ['user__username', 'user__email', 'phone', 'document_number']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Usuario', {
            'fields': ('user',)
        }),
        ('Información Personal', {
            'fields': (
                'phone', 'document_type', 'document_number', 'birth_date'
            )
        }),
        ('Dirección', {
            'fields': (
                'address', 'city', 'department', 'postal_code', 'country'
            )
        }),
        ('Perfil', {
            'fields': ('avatar',)
        }),
        ('Preferencias', {
            'fields': (
                'newsletter_subscription', 'email_notifications'
            )
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

