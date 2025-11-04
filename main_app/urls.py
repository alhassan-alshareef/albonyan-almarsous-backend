from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import (
    SignupUserView, ProfileView, LoginView,
    PostListCreateView, PostDetailView,
    PatientDonationListCreateView, PatientDonationDetailView,
    DonationListView, DonationPayView, DonationDetailView,
    PostCommentListCreateView, PostCommentDetailView, PostLikeToggleView,
)

urlpatterns = [
    path('signup/', SignupUserView.as_view(), name='signup'),
    path('login/', LoginView.as_view(), name='login'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path("profile/", ProfileView.as_view(), name="profile"),
    
    path('patient/posts/', PostListCreateView.as_view(), name='patient-posts-list-create'),
    path('patient/posts/<int:post_id>/', PostDetailView.as_view(), name='patient-post-detail'),
    
    path("patient/donations/", PatientDonationListCreateView.as_view(), name="patient-donation-list-create"),
    path("patient/donations/<int:donation_id>/", PatientDonationDetailView.as_view(), name="patient-donation-detail"),
    
    path("donations/", DonationListView.as_view(), name="donation-list"),
    path("donations/<int:donation_id>/", DonationDetailView.as_view(), name="donation-detail"),
    path("donations/<int:donation_id>/pay/", DonationPayView.as_view(), name="donation-pay"),
    
    path("posts/<int:post_id>/comments/", PostCommentListCreateView.as_view(), name="post-comments"),
    path("comments/<int:comment_id>/", PostCommentDetailView.as_view(), name="comment-detail"),

    path("posts/<int:post_id>/like/", PostLikeToggleView.as_view(), name="post-like"),
]
