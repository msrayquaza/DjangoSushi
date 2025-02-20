from django.db import models
from django.core.validators import MinValueValidator, MaxLengthValidator

# Modelo de Usuarios (Empleados que atienden pedidos)
class Usuario(models.Model):
    usuario = models.CharField(max_length=50, unique=True)
    contrasena = models.CharField(max_length=255)

    def __str__(self):
        return self.usuario

# Modelo de Platillos
class Platillo(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True, null=True, validators=[MaxLengthValidator(500)])
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    ingredientes = models.TextField(blank=True, null=True, validators=[MaxLengthValidator(500)])  # Lista de ingredientes en texto
    imagen = models.ImageField(upload_to='imagenes/platillos/', blank=True, null=True)  # Imagen opcional

    def __str__(self):
        return self.nombre

# Modelo de Ventas
class Venta(models.Model):
    TIPOS_VENTA = [
        ('tienda', 'Tienda'),
        ('para llevar', 'Para Llevar'),
        ('plataforma', 'Plataforma'),
    ]
    
    ESTADOS_VENTA = [
        ('pendiente', 'Pendiente'),
        ('completado', 'Completado'),
    ]

    fecha = models.DateTimeField(auto_now_add=True)
    total = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    tipo = models.CharField(max_length=15, choices=TIPOS_VENTA)
    usuario = models.ForeignKey(Usuario, on_delete=models.PROTECT, null=True, blank=True)
    estado = models.CharField(max_length=10, choices=ESTADOS_VENTA, default='pendiente')

    def __str__(self):
        return f"Venta #{self.id} - {self.get_tipo_display()} - {self.get_estado_display()}"

# Modelo de Tickets (Detalle de la Venta)
class Ticket(models.Model):
    venta = models.ForeignKey(Venta, on_delete=models.CASCADE)
    platillo = models.ForeignKey(Platillo, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField()
    subtotal = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])

    def __str__(self):
        return f"Ticket #{self.id} - {self.platillo.nombre} x{self.cantidad}"