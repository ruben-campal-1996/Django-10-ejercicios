from django.urls import path
from . import views

urlpatterns = [
    path('', views.post_list, name='post_list'),
    path('hola/', views.hola_mundo, name='hola_mundo'),  # Ruta para la vista hola_mundo
    path('post/create/', views.PostCreateView.as_view(), name='post_create'),  # Crear post
    path('post/<int:pk>/', views.PostDetailView.as_view(), name='post_detail'),  # Detalles del post
    path('post/<int:pk>/edit/', views.PostUpdateView.as_view(), name='post_edit'),  # Actualizar post
    path('post/<int:pk>/delete/', views.PostDeleteView.as_view(), name='post_delete'),  # Eliminar post
    path('api/posts/', views.PostListCreateAPIView.as_view(), name='post_list_create'),  # API para listar y crear posts
]