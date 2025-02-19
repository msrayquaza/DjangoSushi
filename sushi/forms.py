from django import forms
from django.forms import ModelForm
from .models import Platillo, PlatilloIngrediente

class SushiForm(ModelForm):
    ingredientes = forms.CharField(
        label="Ingredientes del platillo",
        required=False,
        widget=forms.Textarea(attrs={'readonly': 'readonly', 'rows': 3})  # Campo solo lectura
    )

    class Meta:
        model = Platillo
        fields = ['nombre', 'descripcion', 'precio', 'imagen', 'ingredientes']
        labels = {
            'nombre': 'Nombre del platillo',
            'descripcion': 'Descripción del platillo',
            'precio': 'Precio del platillo',
            'imagen': 'Imagen del platillo',
            'ingredientes': 'Ingredientes del platillo'
        }
        help_texts = {
            'nombre': 'Ingrese el nombre del platillo',
            'descripcion': 'Ingrese una breve descripción del platillo',
            'precio': 'Ingrese el precio del platillo',
            'imagen': 'Seleccione una imagen para el platillo',
            'ingredientes': 'Lista de ingredientes utilizados en este platillo'
        }

    def __init__(self, *args, **kwargs):
        super(SushiForm, self).__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            ingredientes = PlatilloIngrediente.objects.filter(platillo=self.instance)
            if ingredientes.exists():
                self.fields['ingredientes'].initial = "\n".join(
                    [f"{ing.ingrediente.nombre} ({ing.cantidad} {ing.ingrediente.get_unidad_medida_display()})" for ing in ingredientes]
                )
            else:
                self.fields['ingredientes'].initial = "Sin ingredientes registrados aún"
