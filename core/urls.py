from django.urls import path
from .views import HomeView, TestView, CategoriesPageView, LoginPageView, RegisterPageView
urlpatterns = [
    # path('home/', views.home_view, name='home'),
    path('', HomeView.as_view(), name='home'),
    path("test/", TestView.as_view(), name="test"),
    path('login/', LoginPageView.as_view(), name='login'),
    path('register/', RegisterPageView.as_view(), name='register'),
]