from django.urls import path
from . import views

urlpatterns = [
    path('', views.inicio, name='inicio'),
    path('productos/', views.productos, name='productos'),
    path('distribuidor/', views.distribuidor, name='distribuidor'),
    path('contacto/', views.contacto, name='contacto'),

    # 🔥 NUEVAS RUTAS PARA TU SISTEMA DE INGREDIENTES
    path('categoria/<str:categoria>/', views.catalogo_categoria, name='catalogo_categoria'),
    path('seleccionar/', views.seleccionar_ingredientes, name='seleccionar_ingredientes'),

    # ⭐ RUTA QUE MUESTRA LAS 3 RECETAS SUGERIDAS
    path('recetas/', views.ver_recetas, name='recetas_con_ingredientes'),

    # ⭐ RUTA QUE MUESTRA UNA RECETA COMPLETA (la correcta)
    path('receta/<int:receta_id>/', views.receta_completa, name='receta_completa'),

    # ⚡ RUTA DE GUARDAR RECETA
    path('guardar-receta/', views.guardar_receta, name='guardar_receta'),
    path('seleccionar/', views.seleccionar_ingredientes, name='seleccionar_ingredientes'),
    path('limpiar/', views.limpiar_ingredientes, name='limpiar_ingredientes'),


]
