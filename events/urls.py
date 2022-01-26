from . import views
from django.urls import path

urlpatterns = [
    # path('', views.home, name='home')
    path('<int:year>/<str:month>', views.home, name='home')
]
