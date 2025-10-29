from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import SignupUserView,ProfileView, LoginView, PostListCreateView, PostDetailView

urlpatterns = [
    path('signup/', SignupUserView.as_view(), name='signup'),
    path('login/', LoginView.as_view(), name='Login'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path("profile/", ProfileView.as_view(), name="profile"),
    
    path('patient/posts/', PostListCreateView.as_view(), name='patient-posts-list-create'),
    path('patient/posts/<int:post_id>/', PostDetailView.as_view(), name='patient-post-detail'),
]
