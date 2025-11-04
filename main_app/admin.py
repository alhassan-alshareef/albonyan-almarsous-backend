from django.contrib import admin
from .models import UserProfile, Post, Donation, DonationPayment, PostComment, PostLike

admin.site.register(UserProfile)
admin.site.register(Post)
admin.site.register(Donation)
admin.site.register(DonationPayment)
admin.site.register(PostComment)
admin.site.register(PostLike)
