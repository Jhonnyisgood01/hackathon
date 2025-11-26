from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

# Configuramos el admin para que muestre el DNI y el ROL
class CustomUserAdmin(UserAdmin):
    # Campos a mostrar en la lista (columnas)
    list_display = ('username', 'email', 'first_name', 'last_name', 'role', 'dni', 'is_staff')
    
    # Filtros laterales
    list_filter = ('role', 'is_staff', 'is_active')
    
    # Agregamos los campos nuevos al formulario de edición
    fieldsets = UserAdmin.fieldsets + (
        ('Información Bancaria', {'fields': ('role', 'dni', 'phone')}),
    )
    
    # Agregamos los campos nuevos al formulario de creación
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': ('role', 'dni', 'phone')}),
    )

admin.site.register(User, CustomUserAdmin)