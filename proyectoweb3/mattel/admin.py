from django.contrib import admin
from .models import Producto, Contacto
@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ('nombre','categoria','precio')
@admin.register(Contacto)
class ContactoAdmin(admin.ModelAdmin):
    list_display = ('nombre','email','telefono','creado')
    readonly_fields = ('creado',)
