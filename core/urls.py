from django.urls import path
from .views import *
from django.urls import path
from django.contrib.auth import views as auth_views
from core import views as custom_views
from django.urls import path, include

urlpatterns = [
    # path('home/', views.home_view, name='home'),
    path('forgot-password/', custom_views.ForgotPasswordView.as_view(), name='password.request'),
    path('reset-password/<uidb64>/<token>/', custom_views.ResetPasswordView.as_view(), name='password.reset'),
    path('reset-password/', custom_views.ResetPasswordSubmitView.as_view(), name='password.store'),
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
    path('blog/', BlogIndexView.as_view(), name='blog_index'),
    path('contact/', ContactView.as_view(), name='contact'),
    path('newsletter/subscribe/', NewsletterSubscribeView.as_view(), name='newsletter.subscribe'),
    path('comments/<int:comment_id>/like', ToggleLikeView.as_view(), name='comment-like'),
    path('comments/', CommentCreateView.as_view(), name='comments.store'),
    path('comments/<int:comment_id>/', CommentUpdateView.as_view(), name='comments.update'),
    path('comments/<int:comment_id>/delete/', CommentDeleteView.as_view(), name='comments.destroy'),
    path('posts/<int:id>/update/', PostUpdateView.as_view(), name='posts.update'),
    path('posts/<int:id>/delete/', PostDeleteView.as_view(), name='posts.destroy'),
    path('verify/<uidb64>/<token>/', verify_email, name='verify-email'),
]

if settings.DEBUG:
    import debug_toolbar

    urlpatterns += [
        path('__debug__/', include(debug_toolbar.urls)),
    ]
