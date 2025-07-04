import json
from datetime import datetime
from django.template.defaultfilters import slugify
from core.models import Post, Category
from core.serializers import PostSerializer, CommentSerializer
from django.views import View
from django_inertia import Inertia
from django.urls import reverse_lazy
from django.db import IntegrityError
from .forms import RegisterForm
from django.core.mail import send_mail
from django.conf import settings
from django.middleware.csrf import get_token
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.shortcuts import redirect, get_object_or_404
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model, update_session_auth_hash, logout, login, authenticate
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.hashers import check_password
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import RegisterForm
from core.models import Comment


User = get_user_model()


class TestView(View):
    def get(self, request):
        return Inertia.render(request, component='Test', props={'message': 'Zdravo iz Djangoa!'})


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

class BlogIndexView(View):
    def get(self, request):
        query = request.GET.get('q')
        category_name = request.GET.get('category')

        posts = Post.objects.select_related('category', 'user').order_by('-created_at')

        if query:
            posts = posts.filter(
                Q(title__icontains=query) |
                Q(excerpt__icontains=query) |
                Q(category__name__icontains=query)
            )

        if category_name:
            posts = posts.filter(category__name=category_name)

        matched_category = None
        if query:
            matched_category = Category.objects.filter(name__icontains=query).first()

        selected_category = category_name or (matched_category.name if matched_category else None)

        # Use serializer for posts (like you do in HomeView)
        serialized_posts = PostSerializer(posts, many=True).data

        categories = list(Category.objects.all().values('id', 'name'))

        print(serialized_posts)

        return Inertia.render(request, 'Blog/Index', {
            'posts': serialized_posts,
            'categories': categories,
            'searchQuery': query,
            'selectedCategory': selected_category,
            'auth': { 'user': request.user if request.user.is_authenticated else None },
            'footerCategories': categories,
        })

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
                request.session.set_expiry(0)

            return Inertia.location(reverse_lazy('home'))
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
            'errors': {},
            'status': request.session.pop('status', None),
            'csrf_token': csrf_token,
            'old_input': {},
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
                        'Welcome!',
                        'Thanks for joining.',
                        settings.DEFAULT_FROM_EMAIL,
                        [user.email],
                        fail_silently=True,
                    )
                except Exception as e:
                    print(f"Email error: {e}")

                request.session['status'] = 'Registration successful!'
                return Inertia.location(reverse_lazy('home'))

            except IntegrityError:
                return Inertia.render(request, 'Auth/Register', {
                    'errors': {'email': ['User already exists.']},
                    'status': 'Email already in use.',
                    'old_input': data,
                    'csrf_token': get_token(request),  #Re-send token if rendering again
                })

        #Validation failed — always send dict
        return Inertia.render(request, 'Auth/Register', {
            'errors': form.errors.get_json_data() if form.errors else {},
            'status': 'Please correct the errors below.',
            'old_input': data,
            'csrf_token': get_token(request),
        })


class DashboardView(LoginRequiredMixin, View):
    def get(self, request):
        user = request.user
        posts = list(Post.objects.filter(user=user).values(
            'id', 'title', 'body', 'category__name'
        ))
        categories = list(Category.objects.all().values('id', 'name'))

        return Inertia.render(request, 'Dashboard', {
            'auth': {
                'user': {
                    'id': user.id,
                    'email': user.email,
                    'first_name': user.first_name,
                    'last_name': user.last_name,
                }
            },
            'posts': posts,
            'categories': categories,
        })

class ProfileView(LoginRequiredMixin, View):
    def get(self, request):
        user = request.user

        return Inertia.render(request, 'Profile/Edit', {
            'auth': {
                'user': {
                    'id': user.id,
                    'email': user.email,
                    'first_name': user.first_name,
                    'last_name': user.last_name,
                    'theme_color': user.theme_color,
                    'email_verified_at': user.email_verified_at,
                }
            },
            'mustVerifyEmail': user.email_verified_at is None,
            'status': request.GET.get('status', '')
        })


class UpdateProfileView(LoginRequiredMixin, View):
    def post(self, request):
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)

        name = data.get('name', '').strip()
        email = data.get('email', '').strip()
        user = request.user

        errors = {}

        if not name:
            errors['name'] = "Name is required."

        if not email:
            errors['email'] = "Email is required."
        else:
            try:
                validate_email(email)
            except ValidationError:
                errors['email'] = "Invalid email format."
            else:
                if User.objects.exclude(pk=user.pk).filter(email=email).exists():
                    errors['email'] = "Email is already taken."

        if errors:
            return JsonResponse({'errors': errors}, status=422)

        user.first_name = name
        user.email = email
        user.save()

        return JsonResponse({'message': 'Profile updated successfully.'})

class UpdatePasswordView(LoginRequiredMixin, View):
    def post(self, request):
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)

        current_password = data.get('current_password', '')
        new_password = data.get('password', '')
        password_confirmation = data.get('password_confirmation', '')

        user = request.user
        errors = {}

        if not check_password(current_password, user.password):
            errors['current_password'] = "The current password is incorrect."

        if new_password != password_confirmation:
            errors['password_confirmation'] = "The password confirmation does not match."

        try:
            validate_password(new_password, user)
        except ValidationError as e:
            errors['password'] = list(e.messages)

        if errors:
            return JsonResponse({'errors': errors}, status=422)

        user.set_password(new_password)
        user.save()
        update_session_auth_hash(request, user)

        return JsonResponse({'message': 'Password updated successfully.'})

class DeleteAccountView(LoginRequiredMixin, View):
    def post(self, request):
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)

        password = data.get('password', '')
        user = request.user

        if not check_password(password, user.password):
            return JsonResponse({'errors': {'password': 'The password is incorrect.'}}, status=422)

        user.delete()
        return JsonResponse({'message': 'Account deleted successfully.'})

class CreatePostView(LoginRequiredMixin, View):
    def post(self, request):
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)

        title = data.get('title', '').strip()
        body = data.get('content', '').strip()
        category_id = data.get('category_id')
        slug = slugify(title)
        excerpt = body[:250]

        errors = {}

        if not title:
            errors['title'] = 'Title is required.'
        elif Post.objects.filter(slug=slug).exists():
            errors['title'] = 'A post with this title already exists.'

        if not body:
            errors['content'] = 'Content is required.'

        category = None
        if category_id:
            try:
                category = Category.objects.get(id=category_id)
            except Category.DoesNotExist:
                errors['category_id'] = 'Invalid category.'

        if errors:
            return JsonResponse({'errors': errors}, status=422)

        Post.objects.create(
            user=request.user,
            category=category,
            title=title,
            slug=slug,
            excerpt=excerpt,
            body=body,
            published_at=datetime.now()
        )

        return JsonResponse({'message': 'Post created successfully.'})

class PostDetailView(View):
    def get(self, request, post_id):
        try:
            post = Post.objects.select_related('user', 'category').get(id=post_id)
        except Post.DoesNotExist:
            return JsonResponse({'error': 'Post not found'}, status=404)

        serialized_post = PostSerializer(post).data

        top_level_comments = Comment.objects.filter(post_id=post_id, parent=None) \
            .select_related('user').order_by('created_at')

        serialized_comments = CommentSerializer(top_level_comments, many=True).data

        return Inertia.render(request, 'Posts/Show', {
            'post': serialized_post,
            'comments': serialized_comments,
            'user': {
                'id': request.user.id,
                'username': request.user.username,
                'email': request.user.email,
            } if request.user.is_authenticated else None,
            'auth': {
                'user': {
                    'id': request.user.id,
                    'email': request.user.email,
                } if request.user.is_authenticated else None
            }
        })

class CategoryDetailView(View):
    def get(self, request, category_id):
        category = get_object_or_404(Category, id=category_id)
        posts = Post.objects.filter(category=category)
        categories = list(Category.objects.all().values('id', 'name'))

        return Inertia.render(request, 'Categories/Show', {
            'category': {
                'id': category.id,
                'name': category.name,
            },
            'posts': list(posts.values('id', 'title', 'excerpt')),
            'categories': categories,
            'auth': {
                'user': {
                    'id': request.user.id,
                    'email': request.user.email,
                } if request.user.is_authenticated else None
            }
        })

class CategoriesPageView(View):
    def get(self, request):


        categories = []

        for category in Category.objects.all():
            posts = Post.objects.filter(category=category).values(
                'id', 'title', 'excerpt', 'body'
            )

            categories.append({
                'id': category.id,
                'name': category.name,
                'image': category.image.url if category.image else None,
                'posts': [dict(p) for p in posts],
            })

        print({
            'categories': categories,
            'auth': {
                'user': {
                    'id': request.user.id,
                    'email': request.user.email,
                } if request.user.is_authenticated else None
            }
        })

        return Inertia.render(request, 'Categories/Index', {
            'categories': categories,
            'auth': {
                'user': {
                    'id': request.user.id,
                    'email': request.user.email,
                } if request.user.is_authenticated else None
            }
        })

class ContactView(View):
    def get(self, request):
        return Inertia.render(request, 'Contact')