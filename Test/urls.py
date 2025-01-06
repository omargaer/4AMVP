from django.urls import path
from Test import views
app_name = "Test"
urlpatterns = [
    path('', views.auth, name='auth'),
    path('load_menu/', views.load_menu, name='load_menu')
]