# usuarios/admin.py
from django.contrib import admin
from .models import Usuario

@admin.register(Usuario)
class UsuarioAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre', 'correo', 'fecha_registro')
    list_filter = ('fecha_registro',)
    search_fields = ('nombre', 'correo')
    date_hierarchy = 'fecha_registro'