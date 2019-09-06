from django.urls import include, path
from . import views
urlpatterns = [
    path('qrcodes/', views.index, name = "index") 
]
