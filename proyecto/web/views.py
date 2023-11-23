from django.shortcuts import render

from .models import Categoria,Marca,Producto

# Create your views here.
def index(request):
    lista_categorias = Categoria.objects.all()
    lista_marcas = Marca.objects.all()
    lista_productos = Producto.objects.all()

    context = {
        'categorias' : lista_categorias,
        'marcas' : lista_marcas,
        'productos' : lista_productos
    }
    return render(request,'index.html',context)

def productos_por_categoria(request,categoria_id):
    """Vistas para filtrar productos por categoria"""
    obj_categoria = Categoria.objects.get(pk=categoria_id)
    lista_productos = obj_categoria.producto_set.all()
    lista_categorias = Categoria.objects.all()
    lista_marcas = Marca.objects.all()

    context = {
        'categorias' : lista_categorias,
        'marcas' : lista_marcas,
        'productos' : lista_productos
    }
    return render(request, 'index.html', context)

def productos_por_marca(request,marca_id):
    """ vista para filtrar productos por marcas """
    obj_marca = Marca.objects.get(pk=marca_id)
    lista_productos = obj_marca.producto_set.all()
    lista_categorias = Categoria.objects.all()
    lista_marcas = Marca.objects.all()
    
    context  = {
        'categorias':lista_categorias,
        'marcas':lista_marcas,
        'productos':lista_productos
    }
    return render(request,'index.html',context)

def productos_por_nombre(request):
    """ vista para filtrar productos por buscador """
    nombre = request.POST['nombre']
    
    lista_productos = Producto.objects.filter(nombre__icontains=nombre)
    lista_categorias = Categoria.objects.all()
    lista_marcas = Marca.objects.all()
    
    context = {
        'categorias':lista_categorias,
        'marcas':lista_marcas,
        'productos':lista_productos
    }
    return render(request,'index.html',context)

""" esto es para encontrar un solo producto """
def producto(request,producto_id):
    obj_producto = Producto.objects.get(pk=producto_id)
    print(obj_producto)
    context = {
        'producto':obj_producto
    }
    return render(request,'producto.html',context)

""" vistas para carrito de compras """
from .carrito import Cart

def carrito(request):
    return render(request, 'carrito.html')

def agregar_carrito(request,producto_id):
    cantidad = 1

    obj_producto = Producto.objects.get(pk=producto_id)
    carrito = Cart(request)
    carrito.add(obj_producto,cantidad)

    print(request.session.get('cart'))

    return render(request,'carrito.html')