"""
URL configuration for FoodTrackOrder project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from sushi import views

urlpatterns = [
    path('', views.home, name='home'),
    path('admin/', admin.site.urls),
    path('sushi/', views.sushi, name='sushi'),
    path('signin/', views.signin, name='signin'),
    path('signup/', views.signup, name='signup'),
    path('logout/', views.signout, name='logout'),
    path('sushi/create/', views.create_platillo, name='create_platillo'),
    path('sushi/edit/<int:platillo_id>/', views.edit_platillo, name='edit_platillo'),  # <-- Asegúrate de incluir esta línea
    path('sushi/delete/<int:platillo_id>/', views.delete_platillo, name='delete_platillo'),  # <-- Y esta también
    
]

