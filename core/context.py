from core.models import Post, Category
from django_inertia import Inertia
from core.serializers import UserSerializer

def get_auth_user(request):
    return {
        'user': UserSerializer(request.user).data
        if request.user.is_authenticated else None
    }

Inertia.share({
    'auth': get_auth_user,
    'categories': lambda request: list(Category.objects.values('id', 'name'))
})