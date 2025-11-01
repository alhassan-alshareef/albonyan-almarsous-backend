from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()
# Create your models here.


class UserProfile(models.Model):
    ROLE_CHOICES = [
        ('patient', 'Patient'),
        ('supporter', 'Supporter')
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    illness = models.CharField(max_length=100, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.user.username} ({self.role})"
    
    
class Post(models.Model):
    patient = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posts")
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    
    def __str__(self):
        return f"Post by: {self.patient.username}"
    
    class Meta:
        ordering = ['-created_at']

    

class PostComment (models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by: {self.user.username} on Post {self.post.id}"


class PostLike (models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Like by: {self.user.username} on Post {self.post.id}"
    
    

class Donation(models.Model):
    patient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='donations_received')
    title = models.CharField(max_length=50)
    target_amount = models.DecimalField(max_digits=10, decimal_places=2)
    amount_donated = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    
    def __str__(self):
        return f"{self.title} ({self.patient.username})"

    class Meta:
        ordering = ['-created_at']

    
class DonationPayment(models.Model):
    donation = models.ForeignKey(Donation, on_delete=models.CASCADE, related_name='payments')
    supporter = models.ForeignKey(User, on_delete=models.CASCADE, related_name='donations_made')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.supporter.username} donated {self.amount} to {self.donation.title}"