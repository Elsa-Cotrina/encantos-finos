from django.shortcuts import render

from .models import Categoria,Marca,Producto

# Create your views here.
def index(request):
    lista_categorias = Categoria.objects.all()
    lista_marca = Marca.objects.all()
    lista_productos = Producto.objects.all()

    context = {
        'categorias' : lista_categorias,
        'marca' : lista_marca,
        'productos' : lista_productos
    }


    return render(request,'index.html',context)
