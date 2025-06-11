from django_inertia import Inertia
from core.models import Post, Category

Inertia.share({
    'categories': lambda request: list(Category.objects.values('id', 'name'))
})