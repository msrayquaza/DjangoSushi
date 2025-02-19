from django.db import models

# Modelo de Usuarios (Empleados que atienden pedidos)
class Usuario(models.Model):
    usuario = models.CharField(max_length=50, unique=True)
    contrasena = models.CharField(max_length=255)

    def __str__(self):
        return self.usuario

# Modelo de Ingredientes con soporte para diferentes unidades de medida
class Ingrediente(models.Model):
    UNIDADES_MEDIDA = [
        ('pieza', 'Pieza'),
        ('kg', 'Kilogramo'),
        ('g', 'Gramo'),
        ('l', 'Litro'),
        ('ml', 'Mililitro'),
    ]
    
    nombre = models.CharField(max_length=100)
    unidad_medida = models.CharField(max_length=10, choices=UNIDADES_MEDIDA)
    cantidad_por_unidad = models.DecimalField(max_digits=10, decimal_places=2)  # Cantidad que representa esta unidad (Ej: 1 kg = 1000 g)
    imagen = models.ImageField(upload_to='imagenes/ingredientes/', blank=True, null=True)  # Imagen opcional para el ingrediente

    def __str__(self):
        return f"{self.nombre} ({self.cantidad_por_unidad} {self.get_unidad_medida_display()})"

# Modelo de Platillos
class Platillo(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True, null=True)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    imagen = models.ImageField(upload_to='imagenes/platillos/', blank=True, null=True)  # Imagen opcional para el platillo

    def __str__(self):
        return self.nombre

# Modelo intermedio entre Platillos e Ingredientes
class PlatilloIngrediente(models.Model):
    platillo = models.ForeignKey(Platillo, on_delete=models.CASCADE)
    ingrediente = models.ForeignKey(Ingrediente, on_delete=models.CASCADE)
    cantidad = models.DecimalField(max_digits=10, decimal_places=2)  # Cantidad de ingrediente en el platillo

    def __str__(self):
        return f"{self.ingrediente.nombre} en {self.platillo.nombre} ({self.cantidad} {self.ingrediente.unidad_medida})"

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
    total = models.DecimalField(max_digits=10, decimal_places=2)
    tipo = models.CharField(max_length=15, choices=TIPOS_VENTA)
    usuario = models.ForeignKey(Usuario, on_delete=models.SET_NULL, null=True, blank=True)
    estado = models.CharField(max_length=10, choices=ESTADOS_VENTA, default='pendiente')

    def __str__(self):
        return f"Venta #{self.id} - {self.get_tipo_display()} - {self.get_estado_display()}"

# Modelo de Tickets (Detalle de la Venta)
class Ticket(models.Model):
    venta = models.ForeignKey(Venta, on_delete=models.CASCADE)
    platillo = models.ForeignKey(Platillo, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField()
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Ticket #{self.id} - {self.platillo.nombre} x{self.cantidad}"
