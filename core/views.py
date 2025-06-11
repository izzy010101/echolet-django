from time import sleep
from django.views.decorators.csrf import csrf_exempt
from core.models import Post, Category
from core.serializers import PostSerializer
from django.views import View
from django_inertia import Inertia
from django.contrib.auth import login, authenticate
from django.urls import reverse_lazy
from django.db import IntegrityError
from .forms import RegisterForm
from django.core.mail import send_mail
from django.conf import settings
from django.middleware.csrf import get_token
import json
from django.contrib.auth import logout
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.http import HttpResponseRedirect
from django.shortcuts import redirect

class TestView(View):
    def get(self, request):
        return Inertia.render(request, component='Test', props={'message': 'Zdravo iz Djangoa!'})

class CategoriesPageView(View):
    def get(self, request):
        categories = Category.objects.all().values('id', 'name')  # simple serialization

        return Inertia.render(request, 'CategoriesPage', {
            'categories': list(categories),
        })

class HomeView(View):
    def get(self, request):
        posts = Post.objects.order_by('-published_at')[:10]
        serialized_posts = PostSerializer(posts, many=True).data

        featured = serialized_posts[0] if serialized_posts else None
        rest = serialized_posts[1:] if len(serialized_posts) > 1 else []

        return Inertia.render(
            request,
            'Home',
            props={
                'featured': featured,
                'posts': serialized_posts,
            }
        )

class LoginPageView(View):
    def get(self, request):
        return Inertia.render(request, 'Auth/Login', {})

    def post(self, request):
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            data = {}

        email = data.get('email', '').strip()
        password = data.get('password', '')
        remember = data.get('remember', False)

        user = authenticate(request, username=email, password=password)

        if user is not None:
            login(request, user)

            if not remember:
                request.session.set_expiry(0)  # Session expires on browser close

            return Inertia.location(reverse_lazy('home'))  # redirect to homepage
        else:
            return Inertia.render(request, 'Auth/Login', {
                'errors': {
                    'email': 'Invalid email or password.',
                },
                'status': 'Login failed.',
            })

class LogoutView(View):
    @method_decorator(csrf_exempt)
    def post(self, request):
        logout(request)
        return redirect(reverse_lazy('home'))


class RegisterPageView(View):
    def get(self, request):
        csrf_token = get_token(request)
        print(f"DJANGO RENDER: CSRF Token for page load: {csrf_token}")
        return Inertia.render(request, 'Auth/Register', {
            'errors': {}, # Initialize empty errors on GET request
            'status': request.session.pop('status', None),
            'csrf_token': csrf_token,
        })

    def post(self, request):
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            data = {}

        form = RegisterForm(data)

        if form.is_valid():
            try:
                user = form.save()

                login(request, user)

                try:
                    send_mail(
                        'Welcome to My Django App!',
                        'Thank you for registering. We are excited to have you!',
                        settings.DEFAULT_FROM_EMAIL, # Defined in settings.py
                        [user.email],
                        fail_silently=False,
                    )

                except Exception as e:
                    print(f"Error sending welcome email to {user.email}: {e}")

                request.session['status'] = 'Registration successful! Welcome.'

                return Inertia.location(reverse_lazy('home'))

            except IntegrityError:
                return Inertia.render(request, 'Auth/Register', {
                    'errors': {'email': ['A user with that email already exists.']},
                    'status': 'An error occurred during registration.',
                    'old_input': request.POST.dict()
                })

        else:
            print(f"Form errors: {form.errors.as_json()}") # For debugging
            return Inertia.render(request, 'Auth/Register', {
                'errors': form.errors.get_json_data(),
                'status': 'Please correct the errors below.',
                'old_input': request.POST.dict()
            })



