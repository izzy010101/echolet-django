import json
from datetime import datetime
from django.template.defaultfilters import slugify
from core.serializers import PostSerializer, CommentSerializer
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django_inertia import Inertia
from django.urls import reverse_lazy
from django.db import IntegrityError
from .forms import RegisterForm
from django.core.mail import send_mail
from django.conf import settings
from django.middleware.csrf import get_token
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.shortcuts import redirect, get_object_or_404
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model, update_session_auth_hash, logout, login, authenticate
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.hashers import check_password
from django.contrib.auth.mixins import LoginRequiredMixin
from core.models import Comment, NewsletterSubscription, CommentLike, Post, Category
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.core.mail import send_mail
import logging
from django.db.models import Q
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.urls import reverse
from django.core.mail import send_mail
from django.conf import settings
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.forms import PasswordResetForm
User = get_user_model()
from django.contrib.auth.forms import SetPasswordForm
from django.views import View
from django.db import connection

logger = logging.getLogger(__name__)


class ForgotPasswordView(View):
    def get(self, request):
        print("SQL qqueries: ",end="")
        print(len(connection.queries))
        return Inertia.render(request, 'Auth/ForgotPassword', {
            'status': request.session.pop('status', None)
        })

    def post(self, request):
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)

        form = PasswordResetForm(data=data)
        if form.is_valid():
            email = form.cleaned_data['email']
            for user in form.get_users(email):
                token = default_token_generator.make_token(user)
                uid = urlsafe_base64_encode(force_bytes(user.pk))
                reset_url = request.build_absolute_uri(reverse('password.reset', args=[uid, token]))

                send_mail(
                    subject='Reset your password',
                    message=f'Click the link to reset your password: {reset_url}',
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[user.email],
                )

            request.session['status'] = 'Password reset link sent!'
            return JsonResponse({'success': True, 'message': 'Password reset link sent!'})

        return JsonResponse({'errors': form.errors}, status=400)


class ResetPasswordView(View):
    def get(self, request, uidb64, token):
        print("SQL qqueries: ",end="")
        print(len(connection.queries))
        try:
            uid = urlsafe_base64_decode(uidb64).decode()
            user = User.objects.get(pk=uid)
        except Exception:
            user = None

        if user is not None and default_token_generator.check_token(user, token):
            return Inertia.render(request, 'Auth/ResetPassword', {
                'email': user.email,
                'token': token,
            })

        return redirect('password.request')


class ResetPasswordSubmitView(View):
    def post(self, request):
        print("SQL qqueries: ",end="")
        print(len(connection.queries))
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({'errors': {'general': ['Invalid JSON']}}, status=400)

        email = data.get('email')
        token = data.get('token')

        if not email or not token:
            return JsonResponse({'errors': {'general': ['Missing email or token']}}, status=400)

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return JsonResponse({'errors': {'email': ['User not found']}}, status=404)

        if not default_token_generator.check_token(user, token):
            return JsonResponse({'errors': {'token': ['Invalid or expired token']}}, status=400)

        data['new_password1'] = data.pop('password', '')
        data['new_password2'] = data.pop('password_confirmation', '')

        form = SetPasswordForm(user, data)
        if form.is_valid():
            form.save()
            return JsonResponse({'success': True, 'redirect': '/login/'})
        else:
            return JsonResponse({'errors': form.errors}, status=400)

class PostUpdateView(View):
    def put(self, request, id):
        print("SQL qqueries: ",end="")
        print(len(connection.queries))
        post = get_object_or_404(Post, id=id)

        if post.user != request.user:
            return HttpResponseForbidden("You don't have permission to edit this post.")

        data = json.loads(request.body)
        post.title = data.get("title", post.title)
        post.body = data.get("body", post.body)
        post.category_id = data.get("category_id", post.category_id)
        post.save()

        return HttpResponseRedirect('/dashboard/')

class PostDeleteView(View):
    def delete(self, request, id):
        print("SQL qqueries: ",end="")
        print(len(connection.queries))
        post = get_object_or_404(Post, id=id)

        if post.user != request.user:
            return HttpResponseForbidden("You don't have permission to delete this post.")

        post.delete()
        return HttpResponseRedirect('/dashboard/')

class CommentCreateView(LoginRequiredMixin, View):
    def post(self, request):
        print("SQL qqueries: ",end="")
        print(len(connection.queries))
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)

        content = data.get('content', '').strip()
        post_id = data.get('post_id')
        parent_id = data.get('parent_id')

        errors = {}

        if not content:
            errors['content'] = "Content cannot be empty."

        if not post_id or not Post.objects.filter(id=post_id).exists():
            errors['post_id'] = "Invalid post ID."

        if errors:
            return JsonResponse({'errors': errors}, status=422)

        comment = Comment.objects.create(
            user=request.user,
            post_id=post_id,
            parent_id=parent_id,
            content=content
        )

        return HttpResponseRedirect('/posts/'+str(post_id))

class CommentUpdateView(LoginRequiredMixin, View):
    def put(self, request, comment_id):
        print("SQL qqueries: ",end="")
        print(len(connection.queries))
        try:
            comment = Comment.objects.get(id=comment_id, user=request.user)
        except Comment.DoesNotExist:
            return JsonResponse({'error': 'Comment not found or permission denied.'}, status=404)

        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)

        content = data.get('content', '').strip()

        if not content:
            return JsonResponse({'errors': {'content': 'Content cannot be empty.'}}, status=422)

        comment.content = content
        comment.save()

        return HttpResponseRedirect('/posts/'+str(comment.post.id))

class CommentDeleteView(LoginRequiredMixin, View):
    def delete(self, request, comment_id):
        print("SQL qqueries: ",end="")
        print(len(connection.queries))
        try:
            comment = Comment.objects.get(id=comment_id, user=request.user)
        except Comment.DoesNotExist:
            return JsonResponse({'error': 'Comment not found or permission denied.'}, status=404)

        id = comment.post.id

        comment.delete()
        return HttpResponseRedirect('/posts/'+str(id))

class TestView(View):
    def get(self, request):
        print("SQL qqueries: ",end="")
        print(len(connection.queries))
        return Inertia.render(request, component='Test', props={'message': 'Zdravo iz Djangoa!'})


class HomeView(View):
    def get(self, request):
        print("SQL qqueries: ",end="")
        print(len(connection.queries))

        query = request.GET.get('q', '').strip()

        if query:
            posts = Post.objects.filter(
                Q(title__icontains=query) |
                Q(body__icontains=query)
            ).order_by('-published_at')[:10]
        else:
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
                'query': query or '',
            }
        )

class BlogIndexView(View):
    def get(self, request):
        print("SQL qqueries: ",end="")
        print(len(connection.queries))

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

        serialized_posts = PostSerializer(posts, many=True).data

        categories = list(Category.objects.all().values('id', 'name'))

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
        print("SQL qqueries: ",end="")
        print(len(connection.queries))
        return Inertia.render(request, 'Auth/Login', {})

    def post(self, request):
        print("SQL qqueries: ",end="")
        print(len(connection.queries))
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
        print("SQL qqueries: ",end="")
        print(len(connection.queries))
        logout(request)
        return redirect(reverse_lazy('home'))


class RegisterPageView(View):
    def get(self, request):
        print("SQL qqueries: ",end="")
        print(len(connection.queries))

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
                user = form.save(commit=False)
                user.is_active = False
                user.save()
                # login(request, user)

                try:
                    token = default_token_generator.make_token(user)
                    uid = urlsafe_base64_encode(force_bytes(user.pk))

                    verify_url = request.build_absolute_uri(
                        reverse('verify-email', args=[uid, token])
                    )

                    send_mail(
                        subject='Verify Your Email',
                        message=f'Click the link to verify your email: {verify_url}',
                        from_email=settings.DEFAULT_FROM_EMAIL,
                        recipient_list=[user.email],
                        fail_silently=False,
                    )

                    return redirect('login')
                except Exception as e:
                    print(f"Email error: {e}")

                request.session['status'] = 'Registration successful!'
                return Inertia.location(reverse_lazy('home'))

            except IntegrityError as e:
                print("Integrity Error")
                print(e)
                return Inertia.render(request, 'Auth/Register', {
                    'errors': {'email': ['User already exists.']},
                    'status': 'Email already in use.',
                    'old_input': data,
                    'csrf_token': get_token(request),
                })

        return Inertia.render(request, 'Auth/Register', {
            'errors': form.errors.get_json_data() if form.errors else {},
            'status': 'Please correct the errors below.',
            'old_input': data,
            'csrf_token': get_token(request),
        })

def verify_email(request, uidb64, token):
    print("SQL qqueries: ", end="")
    print(len(connection.queries))

    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()

        send_mail(
            subject="Welcome!",
            message="Thank you for verified Email.",
            from_email="noreply@example.com",
            recipient_list=[user.email],
            fail_silently=False,
        )
        print("email sent to user: "+str(user.email))
        messages.success(request, 'Email verified successfully. You can now log in.')
    else:
        messages.error(request, 'Verification link is invalid or expired.')

    return redirect('login')


class DashboardView(LoginRequiredMixin, View):
    def get(self, request):
        print("SQL qqueries: ",end="")
        print(len(connection.queries))
        user = request.user
        query = request.GET.get('q', '').strip().lower()

        all_posts = Post.objects.filter(user=user)

        if query:
            all_posts = all_posts.filter(
                Q(title__icontains=query) | Q(body__icontains=query)
            )

        posts = list(all_posts.values(
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
        print("SQL qqueries: ",end="")
        print(len(connection.queries))
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
        print("SQL qqueries: ",end="")
        print(len(connection.queries))
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

        messages.success(request, "Profile updated successfully.")

        return redirect(request.META.get('HTTP_REFERER', '/profile'))

class UpdatePasswordView(LoginRequiredMixin, View):
    def post(self, request):
        print("SQL qqueries: ",end="")
        print(len(connection.queries))
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
            JsonResponse({'errors': {'content': 'Content cannot be empty.'}}, status=422)

        user.set_password(new_password)
        user.save()
        update_session_auth_hash(request, user)

        return HttpResponseRedirect('/profile/')

class DeleteAccountView(LoginRequiredMixin, View):
    def post(self, request):
        print("SQL qqueries: ",end="")
        print(len(connection.queries))
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
        print("SQL qqueries: ",end="")
        print(len(connection.queries))
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

        return HttpResponseRedirect('/dashboard/')

class PostDetailView(View):
    def get(self, request, post_id):
        print("SQL qqueries: ",end="")
        print(len(connection.queries))
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
        print("SQL qqueries: ",end="")
        print(len(connection.queries))

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
        print("SQL qqueries: ",end="")
        print(len(connection.queries))

        query = request.GET.get('q', '').strip()
        categories = []

        for category in Category.objects.all():
            if query and query not in category.name.lower():
                continue

            posts = Post.objects.filter(category=category).values(
                'id', 'title', 'excerpt', 'body'
            )

            categories.append({
                'id': category.id,
                'name': category.name,
                'image': category.image.url if category.image else None,
                'posts': [dict(p) for p in posts],
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
        print("SQL qqueries: ",end="")
        print(len(connection.queries))
        return Inertia.render(request, 'Contact')

class NewsletterSubscribeView(View):
    def post(self, request):
        print("SQL qqueries: ",end="")
        print(len(connection.queries))

        email = request.POST.get('email', '').strip()

        print(email)

        try:
            validate_email(email)
        except ValidationError:
            return JsonResponse({'message': 'Please enter a valid email address.'}, status=400)

        if NewsletterSubscription.objects.filter(email=email).exists():
            return JsonResponse({'message': 'You are already subscribed.'}, status=200)

        NewsletterSubscription.objects.create(email=email)

        try:
            send_mail(
                subject="Welcome to our Newsletter!",
                message="Thank you for subscribing.",
                from_email="newsletter@example.com",
                recipient_list=[email],
                fail_silently=False,
            )
        except Exception as e:
            logger.error(f"Email sending failed: {e}")
            return JsonResponse({'message': 'Subscription saved, but failed to send email.'}, status=500)

        return JsonResponse({'message': 'Thanks for subscribing!'}, status=200)

class ToggleLikeView(LoginRequiredMixin, View):
    def post(self, request, comment_id):
        print("SQL qqueries: ",end="")
        print(len(connection.queries))

        try:
            comment = Comment.objects.get(id=comment_id)
        except Comment.DoesNotExist:
            return JsonResponse({'error': 'Comment not found'}, status=404)

        like, created = CommentLike.objects.get_or_create(
            user=request.user,
            comment=comment
        )

        if not created:
            like.delete()
            liked = False
        else:
            liked = True

        return JsonResponse({
            'liked': liked,
            'likes_count': comment.likes.count()
        })
