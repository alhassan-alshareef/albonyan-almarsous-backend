from django.contrib import admin
from .models import UserProfile, Post, Donation, DonationPayment

admin.site.register(UserProfile)
admin.site.register(Post)
admin.site.register(Donation)
admin.site.register(DonationPayment)
