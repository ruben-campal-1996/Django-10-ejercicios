from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth import login
from django.urls import reverse_lazy
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.generic import FormView
from .models import Post
from .serializers import PostSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

# Create your views here.

def post_list(request):
    posts=Post.objects.all().order_by('-fecha_creacion')
    return render(request, 'blog/index.html', {'posts': posts})

def hola_mundo(request):
    return HttpResponse("¡Hola, Mundo!")

class PostListView(ListView):
    model = Post
    template_name = 'blog/post_list.html'
    context_object_name = 'posts'

class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/post_detail.html'
    context_object_name = 'post'

class PostCreateView(CreateView):
    model = Post
    template_name = 'blog/post_form.html'  # Plantilla para el formulario de creación
    fields = ['titulo', 'contenido']  # Campos que el usuario podrá llenar
    success_url = reverse_lazy('post_list')  # Redirige a la lista de posts después de crear uno

# Vista para actualizar un post existente
class PostUpdateView(UpdateView):
    model = Post
    template_name = 'blog/post_form.html'
    fields = ['titulo', 'contenido']
    success_url = reverse_lazy('post_list')

    def get_success_url(self):
        return reverse_lazy('post_detail', kwargs={'pk':self.object.pk})

# Vista para eliminar un post
class PostDeleteView(DeleteView):
    model = Post
    template_name = 'blog/post_confirm_delete.html'

    def get_success_url(self):
        return reverse_lazy('post_list')

class RegisterView(FormView):
    template_name = 'Registration/register.html'
    form_class = UserCreationForm
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        # Guardar el usuario y loguearlo automáticamente
        user = form.save()
        print("Formulario válido, guardando usuario")
        login(self.request, user)  # Iniciar sesión automáticamente después del registro
        return super().form_valid(form)

    def form_invalid(self, form):
        print("Formulario no válido")
        print(form.errors)
        return super().form_invalid(form)

# Vista personalizada para login (si deseas personalizarla)
class CustomLoginView(LoginView):
    template_name = 'Registration/login.html'
    redirect_authenticated_user = True  # Si el usuario ya está logueado, redirige al 'post_list'

# Vista personalizada para logout (si deseas personalizarla)
class CustomLogoutView(LogoutView):
    next_page = reverse_lazy('post_list')  # Redirigir a la página principal después de cerrar sesión
    template_name = 'blog/logout.html'


class PostListCreateAPIView(APIView):
    def get(self, request):
        posts = Post.objects.all()  # Obtén todos los posts de la base de datos
        serializer = PostSerializer(posts, many=True)  # Serializa los datos
        return Response(serializer.data)  # Devuelve la respuesta en formato JSON

    def post(self, request):
        serializer = PostSerializer(data=request.data)  # Recibe los datos del post
        if serializer.is_valid():  # Verifica que los datos sean válidos
            serializer.save()  # Guarda el nuevo post
            return Response(serializer.data, status=status.HTTP_201_CREATED)  # Devuelve la respuesta con el nuevo post
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)  # Si hay errores, devuelve 400
