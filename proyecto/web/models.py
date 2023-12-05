from django.db import models

from cloudinary.models import CloudinaryField

# Create your models here.
class Categoria(models.Model):
    nombre = models.CharField(max_length=200)
    fecha_registro = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'tbl_categoria'
        
    def __str__(self):
        return self.nombre
    
class Marca(models.Model):
    nombre = models.CharField(max_length=200)
    fecha_registro = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'tbl_marca'
        
    def __str__(self):
        return self.nombre
    
class Producto(models.Model):
    PAIS = 'Perú'
    SEXO_CHOICES = {
        ('h' , 'men'),
        ('m' , 'women'),
        ('c' , 'children')
    }
    MATERIAL_CHOICES = {
        ('o' , 'oro'),
        ('p' , 'plata'),
        ('c' , 'cobre')
    }

    categoria = models.ForeignKey(Categoria,on_delete=models.RESTRICT)
    marca = models.ForeignKey(Marca,on_delete=models.RESTRICT)
    nombre = models.CharField(max_length=254)
    descripcion = models.TextField(null=True)
    precio = models.DecimalField(max_digits=5,decimal_places=2)
    imagen = CloudinaryField('image',default='')
    sexo = models.CharField(max_length=1,default='m',choices=SEXO_CHOICES)
    dimensiones = models.CharField(max_length=100, default="30 x 10 cm")
    cantidad = models.IntegerField(default=0)
    peso = models.DecimalField(max_digits=5,decimal_places=2)
    pais = models.CharField(max_length=100, default=PAIS, editable=False)
    material = models.CharField(max_length=1,default='o',choices=MATERIAL_CHOICES)
    
    class Meta:
        db_table = 'tbl_producto'
        
    def __str__(self):
        return self.nombre  

from django.contrib.auth.models import User   

class Cliente(models.Model):
    usuario = models.OneToOneField(User,on_delete=models.RESTRICT)
    dni = models.CharField(max_length=8)
    telefono = models.CharField(max_length=50)
    fecha_nacimiento = models.DateField(null= True)
    direccion = models.TextField()

    class Meta:
        db_table = 'tbl_cliente'

    def __str__(self):
        return self.dni   

class Factura(models.Model):
    ESTADO_CHOICES = {
        ('s' , 'SOLICITADO'),
        ('p' , 'PAGADO')
    }
    cliente = models.ForeignKey(Cliente,on_delete=models.RESTRICT)
    fecha_registro = models.DateTimeField(auto_now_add=True)
    monto_total = models.DecimalField(max_digits=5,decimal_places=2,default=0)
    direccion_envio = models.TextField(null=True) 
    estado = models.CharField(max_length=1,default='s',choices=ESTADO_CHOICES)
    nro_pedido = models.CharField(max_length=20,null=True)
    
    class Meta:
        db_table = 'tbl_factura'
    
    def __str__(self):
        return self.nro_pedido

class FacturaDetalle(models.Model):
    factura = models.ForeignKey(Factura,on_delete=models.RESTRICT)
    producto = models.ForeignKey(Producto,on_delete=models.RESTRICT)
    cantidad = models.IntegerField(default=1)
    precio = models.DecimalField(max_digits=5,decimal_places=2)
    subtotal = models.DecimalField(max_digits=5,decimal_places=2)

    class Meta:
        db_table = 'tbl_factura_detalle'

    def __str__(self):
        return self.producto.nombre

    




