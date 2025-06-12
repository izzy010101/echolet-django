from django.urls import path
from .views import HomeView, TestView, CategoriesPageView, LoginPageView, RegisterPageView, LogoutView, DashboardView, \
    ProfileView, UpdateProfileView, UpdatePasswordView, DeleteAccountView, CreatePostView, PostDetailView, \
    CategoryDetailView

urlpatterns = [
    # path('home/', views.home_view, name='home'),
    path('', HomeView.as_view(), name='home'),
    path("test/", TestView.as_view(), name="test"),
    path('login/', LoginPageView.as_view(), name='login'),
    path('register/', RegisterPageView.as_view(), name='register'),
    path("logout/", LogoutView.as_view(), name="logout"),
    path('dashboard/', DashboardView.as_view(), name='dashboard'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('profile/update', UpdateProfileView.as_view(), name='profile.update'),
    path('password/update', UpdatePasswordView.as_view(), name='password.update'),
    path('profile/delete', DeleteAccountView.as_view(), name='profile.destroy'),
    path('posts/store', CreatePostView.as_view(), name='posts.store'),
    path('posts/<int:post_id>/', PostDetailView.as_view(), name='posts_show'),
    path('categories/', CategoriesPageView.as_view(), name='categories.index'),
    path('categories/<int:category_id>/', CategoryDetailView.as_view(), name='categories.show'),
]