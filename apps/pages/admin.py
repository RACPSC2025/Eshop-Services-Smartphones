from django.contrib import admin
from .models import About, Banner


@admin.register(About) 
class AboutAdmin(admin.ModelAdmin):

    def has_change_permission(self, request, obj=None):
        return request.user.is_staff
    def has_add_permission(self, request):
        return request.user.is_superuser
    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser
    def has_view_permission(self, request, obj=None):
        return request.user.is_staff

    list_display = ('title_info', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('title_info',)
    list_editable = ('is_active',)
    readonly_fields = ('created_at', 'updated_at')
    
@admin.register(Banner)
class BannerAdmin(admin.ModelAdmin):
    list_display = ('title', 'is_active', 'position', 'created_at')
    list_filter = ('is_active',)
    search_fields = ('title', 'link')
    list_editable = ('is_active', 'position')
    readonly_fields = ('created_at', 'updated_at')
    
    def has_module_permission(self, request):
        return request.user.is_staff
    
    def has_add_permission(self, request):
        return request.user.is_staff
    
    def has_change_permission(self, request, obj=None):
        return request.user.is_staff
    
    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser
    