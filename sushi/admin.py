from django.contrib import admin
from .models import Platillo, Ingrediente, PlatilloIngrediente

admin.site.register(Platillo)
admin.site.register(Ingrediente)
admin.site.register(PlatilloIngrediente)