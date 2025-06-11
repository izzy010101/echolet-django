from time import sleep

from core.models import Post, Category
from core.serializers import PostSerializer
from django.views import View
from django_inertia import Inertia

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
        pass


class RegisterPageView(View):
    def get(self, request):
        return Inertia.render(request, 'Auth/Register', {})


