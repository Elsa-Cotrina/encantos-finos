from django.contrib.auth import login, logout, authenticate
from .models import Factura
from .forms import ClienteForm
from django.contrib.auth.models import User
from django.urls import reverse
from paypal.standard.forms import PayPalPaymentsForm
from .models import FacturaDetalle
from django.shortcuts import redirect
from .models import Cliente
from django.contrib.auth.decorators import login_required
from .carrito import Cart
from django.shortcuts import render

from .models import Categoria, Marca, Producto

# Create your views here.


def index(request):
    return render(request, 'index.html')

def contactanos(request):
    return render(request, 'contactanos.html')

def sobre_nosotros(request):
    return render(request, 'about.html')

def mi_galeria(request):
    lista_productos = Producto.objects.all()

    context = {
        'productos': lista_productos
    }
    return render(request, 'galeria.html', context)


def shop(request, id):
    lista_categorias = Categoria.objects.all()
    lista_marcas = Marca.objects.all()
    productos_por_pagina = 10  # Cantidad de productos por página
    id = int(id)
    start_index = (id - 1) * productos_por_pagina
    end_index = id * productos_por_pagina
    lista_productos = Producto.objects.all()[start_index:end_index]

    context = {
        'categorias': lista_categorias,
        'marcas': lista_marcas,
        'productos': lista_productos
    }
    return render(request, 'shop.html', context)


def productos_por_categoria(request, categoria_id):
    """Vistas para filtrar productos por categoria"""
    obj_categoria = Categoria.objects.get(pk=categoria_id)
    lista_productos = obj_categoria.producto_set.all()
    lista_categorias = Categoria.objects.all()
    lista_marcas = Marca.objects.all()

    context = {
        'categorias': lista_categorias,
        'marcas': lista_marcas,
        'productos': lista_productos
    }
    return render(request, 'shop.html', context)


def productos_por_marca(request, marca_id):
    """ vista para filtrar productos por marcas """
    obj_marca = Marca.objects.get(pk=marca_id)
    lista_productos = obj_marca.producto_set.all()
    lista_categorias = Categoria.objects.all()
    lista_marcas = Marca.objects.all()

    context = {
        'categorias': lista_categorias,
        'marcas': lista_marcas,
        'productos': lista_productos
    }
    return render(request, 'index.html', context)


def productos_por_nombre(request):
    """ vista para filtrar productos por buscador """
    nombre = request.POST['nombre']

    lista_productos = Producto.objects.filter(nombre__icontains=nombre)
    lista_categorias = Categoria.objects.all()
    lista_marcas = Marca.objects.all()

    context = {
        'categorias': lista_categorias,
        'marcas': lista_marcas,
        'productos': lista_productos
    }
    return render(request, 'index.html', context)


""" esto es para encontrar un solo producto """
def producto(request, producto_id):
    obj_producto = Producto.objects.get(pk=producto_id)
    context = {
        'producto': obj_producto
    }
    return render(request, 'producto.html', context)


""" vistas para carrito de compras """


def carrito(request):
    return render(request, 'carrito.html')


def agregar_carrito(request, producto_id):
    if request.method == 'POST':
        cantidad = int(request.POST['cantidad'])
    else:
        cantidad = 1

    obj_producto = Producto.objects.get(pk=producto_id)
    carrito = Cart(request)
    carrito.add(obj_producto, cantidad)

    print(request.session.get('cart'))

    return render(request, 'carrito.html')


def eliminar_carrito(request, producto_id):
    obj_producto = Producto.objects.get(pk=producto_id)
    carrito = Cart(request)
    carrito.delete(obj_producto)

    return render(request, 'carrito.html')


def limpiar_carrito(request):
    carrito = Cart(request)
    carrito.clear()
    
    return render(request,'carrito.html')


""" VISTAS  PARA CLIENTES """
def crear_usuario(request):
    pagina_destino = request.GET.get('next', None)
    context = {
        'destino': pagina_destino
    }
    if request.method == 'POST':
        data_usuario = request.POST['usuario']
        data_password = request.POST['password']
        data_destino = request.POST['destino']

        usuario = User.objects.create_user(
            username=data_usuario, password=data_password)
        if usuario is not None:
            login(request, usuario)
            if data_destino != 'None':
                return redirect(data_destino)

            return redirect('/cuenta')

    return render(request, 'login.html')


def login_usuario(request):
    pagina_destino = request.GET.get('next', None)
    context = {
        'destino': pagina_destino
    }
    if request.method == 'POST':
        data_usuario = request.POST['usuario']
        data_password = request.POST['password']
        data_destino = request.POST['destino']
        # print(data_destino)

        usuario = authenticate(
            request, username=data_usuario, password=data_password)
        if usuario is not None:
            login(request, usuario)
            if data_destino != 'None':
                return redirect(data_destino)

            return redirect('/cuenta')
        else:
            context = {
                'mensaje_error': 'Intentalo de nuevo',
                'destino': data_destino
            }
    return render(request, 'login.html', context)


@login_required(login_url='/login')
def cuenta_usuario(request):
    try:
        cliente = Cliente.objects.get(usuario=request.user)

        data_cliente = {
            'nombre': request.user.first_name,
            'apellidos': request.user.last_name,
            'email': request.user.email,
            'direccion': cliente.direccion,
            'telefono': cliente.telefono,
            'dni': cliente.dni,
            'fecha_nacimiento': cliente.fecha_nacimiento
        }
    except:
        data_cliente = {
            'nombre': request.user.first_name,
            'apellidos': request.user.last_name,
            'email': request.user.email
        }
    form = ClienteForm(data_cliente)
    context = {
        'form': form
    }
    return render(request, 'cuenta.html', context)


@login_required(login_url='/login')
def logout_usuario(request):
    logout(request)
    return redirect('/cuenta')


@login_required(login_url='/login')
def actualizar_cliente(request):
    mensaje_confirmacion = " "
    frm_cliente = ClienteForm(request.POST)
    if frm_cliente.is_valid():
        # actualizar usuario
        data_cliente = frm_cliente.cleaned_data
        usuario = User.objects.get(pk=request.user.id)
        usuario.first_name = data_cliente['nombre']
        usuario.last_name = data_cliente['apellidos']
        usuario.email = data_cliente['email']
        usuario.save()
        # actualizar o registrar cliente
        try:
            cliente = Cliente.objects.get(usuario=usuario)
        except Exception as error:
            print('error :', error)
            cliente = Cliente()
            cliente.usuario = usuario

        cliente.dni = data_cliente['dni']
        cliente.direccion = data_cliente['direccion']
        cliente.telefono = data_cliente['telefono']
        cliente.fecha_nacimiento = data_cliente['fecha_nacimiento']
        cliente.save()
        mensaje_confirmacion = 'Datos actualizados'

        frm_cliente = ClienteForm()

    context = {
        'form': frm_cliente,
        'mensaje': mensaje_confirmacion
    }
    return render(request, 'cuenta.html', context)


@login_required(login_url='/login')
def confirmar_factura(request):
    try:
        cliente = Cliente.objects.get(usuario=request.user)

        data_cliente = {
            'nombre': request.user.first_name,
            'apellidos': request.user.last_name,
            'email': request.user.email,
            'direccion': cliente.direccion,
            'telefono': cliente.telefono,
            'dni': cliente.dni,
            'fecha_nacimiento': cliente.fecha_nacimiento
        }
    except:
        data_cliente = {
            'nombre': request.user.first_name,
            'apellidos': request.user.last_name,
            'email': request.user.email
        }
    form = ClienteForm(data_cliente)
    context = {
        'form': form
    }
    return render(request, 'factura.html', context)


@login_required(login_url='/login')
def registrar_pedido(request):
    context = {}
    if request.method == 'POST':
        # print('metodo')
        # gestion del usuario y cliente
        data_cliente = request.POST
        usuario = User.objects.get(pk=request.user.id)
        usuario.first_name = data_cliente['nombre']
        usuario.last_name = data_cliente['apellidos']
        usuario.email = data_cliente['email']
        usuario.save()
        try:
            cliente = Cliente.objects.get(usuario=usuario)
            cliente.telefono = data_cliente['telefono']
            cliente.direccion = data_cliente['direccion']
            cliente.save()
        except:
            cliente = Cliente()
            cliente.usuario = usuario
            cliente.direccion = data_cliente['direccion']
            cliente.telefono = data_cliente['telefono']
            cliente.save()

        pedido = Factura()
        pedido.cliente = cliente
        pedido.direccion_envio = data_cliente['direccion']
        pedido.save()

        # registrar pedido detalle
        carrito = Cart(request)
        for key, value in carrito.cart.items():
            producto = Producto.objects.get(pk=value['producto_id'])
            pedido_detalle = FacturaDetalle()
            pedido_detalle.factura = pedido
            pedido_detalle.producto = producto
            pedido_detalle.cantidad = int(value['cantidad'])
            pedido_detalle.precio = float(value['precio'])
            pedido_detalle.subtotal = float(value['subtotal'])
            pedido_detalle.save()

        # limpiamos el carrito
        carrito.clear()

        nro_pedido = 'PED' + str(pedido.id)
        pedido.nro_pedido = nro_pedido
        pedido.monto_total = carrito.total
        pedido.save()

# configuramos formulario paypal
        paypal_dict = {
            "business": "sb-6va47l27985629@business.example.com",
            "amount": pedido.monto_total,
            "item_name": "pedido tienda online",
            "invoice": pedido.nro_pedido,
            "notify_url": request.build_absolute_uri(reverse('paypal-ipn')),
            "return": request.build_absolute_uri('/pedidopagado'),
            "cancel_return": request.build_absolute_uri('/')
        }
    # Create the instance.
    paypal_form = PayPalPaymentsForm(initial=paypal_dict)
    request.session['pedido_id'] = pedido.id

    context = {
        'pedido': pedido,
        'paypal_form': paypal_form
    }

    return render(request, 'pago.html', context)


@login_required(login_url='/login')
def pedido_pagado(request):
    context = {}
    pedido = Factura.objects.get(pk=request.session.get('pedido_id'))
    pedido.estado = 'P'
    pedido.save()
    context = {
        'pedido': pedido
    }
    return render(request, 'pedidopagado.html', context)


""" solicitar por correo  """
from django.core.mail import EmailMessage 
from django.http import HttpResponse
def correo(request):
    if request.method == "POST":
        print("Es valido")
        nombre = request.POST.get("nombre")
        email = request.POST.get("email")
        contenido = request.POST.get("contenido")
        print(nombre, email, contenido)
        email = EmailMessage("Mensaje de app Encantos Finos",
                             "El usuario con nombre {} con la dirección {} escribe lo siguiente:\n\n {}".format(nombre, email, contenido),
                             '',
                             ["encantos.finos@gmail.com"],
                             reply_to=[email])
        try:
            email.send()
        except Exception as e:
            return HttpResponse(f"Error al enviar el correo: {str(e)}")
    return render(request, "index.html")
