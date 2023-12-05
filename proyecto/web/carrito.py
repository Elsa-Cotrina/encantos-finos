class Cart:

    def __init__(self, request):
        self.request = request
        self.session = request.session

        cart = self.session.get('cart')
        total = self.session.get('total')
        if not cart:
            cart = self.session['cart'] = {}
            total = self.session['total'] = '0'

        self.cart = cart
        self.total = float(total)

    def add(self, producto, cantidad):
        if (str(producto.id) not in self.cart.keys()):
            self.cart[producto.id] = {
                'producto_id': producto.id,
                'nombre': producto.nombre,
                'cantidad': cantidad,
                'precio': str(producto.precio),
                'imagen': producto.imagen.url,
                'categoria': producto.categoria.nombre,
                'subtotal': str(cantidad * producto.precio)
            }
        else:
            for key, value in self.cart.items():
                if key == str(producto.id):
                    value['cantidad'] = str(int(value['cantidad']) + cantidad)
                    value['subtotal'] = str(
                        float(value['cantidad']) * float(value['precio']))
                    break

        self.save()

    def delete(self, producto):
        producto_id = str(producto.id)
        if producto_id in self.cart:
            del self.cart[producto_id]
            self.save()

    def clear(self):
        self.session['cart'] = {}
        self.session['total'] = '0'

    def save(self):
        total = 0
        for key, value in self.cart.items():
            total += round(float(value['subtotal']), 2)

        self.session['cart'] = self.cart
        self.session['total'] = total
        self.session.modified = True


    def update(self, producto_id, nueva_cantidad):
        producto_id = str(producto_id)

        if producto_id in self.cart:
            self.cart[producto_id]['cantidad'] = nueva_cantidad
            self.cart[producto_id]['subtotal'] = str(
                float(nueva_cantidad) * float(self.cart[producto_id]['precio']))

        self.save()


    def get_subtotal(self, producto_id):
        producto_id = str(producto_id)
        if producto_id in self.cart:
            return self.cart[producto_id]['subtotal']
        return 0  # Cambia esto por el valor predeterminado si no se encuentra el producto en el carrito
