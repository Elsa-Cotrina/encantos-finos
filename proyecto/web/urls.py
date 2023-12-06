from django.urls import path

from . import views

app_name = 'web'

urlpatterns = [
    path('', views.index,name='index'),
    path('shop/<int:id>', views.shop,name='shop'),
    path('categoria/<int:categoria_id>', views.productos_por_categoria,name='categoria'),
    path('marca/<int:marca_id>', views.productos_por_marca,name='marca'),
    path('buscar', views.productos_por_nombre, name='buscar'),
    path('producto/<int:producto_id>',views.producto,name='producto'),
    path('carrito', views.carrito , name='carrito'),
    path('carrito/add/<int:producto_id>',views.agregar_carrito, name='carritoadd'),
    path('carrito/del/<int:producto_id>',views.eliminar_carrito,name='carritodel'),
    path('carritoclear', views.limpiar_carrito,name='carritoclear'),
    path('usuario/add',views.crear_usuario,name='usuarioadd'),
    path('cuenta', views.cuenta_usuario,name='cuenta'),
    path('login',views.login_usuario,name='usuariologin'),
    path('logout',views.logout_usuario,name='usuariologout'),
    path('cliente/update',views.actualizar_cliente,name='clienteupdate'),
    path('factura',views.confirmar_factura,name='factura'),
    path('registrarpedido',views.registrar_pedido,name='registrarpedido'),
    path('pedidopagado', views.pedido_pagado,name='pedidopagado'),
    path('contactanos', views.contactanos,name='contactanos'),
    path('about', views.sobre_nosotros,name='about'),
    path('galeria', views.mi_galeria,name='galeria'),
    path('senddata',views.correo,name='senddata'),
    path('actualizar_cantidad/', views.actualizar_cantidad, name='actualizar_cantidad'),
]