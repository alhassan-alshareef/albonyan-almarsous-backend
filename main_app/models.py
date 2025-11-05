from django.db import models
from django.contrib.auth import get_user_model
from django.db.models import Sum
from django.core.exceptions import ValidationError


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
    image = models.ImageField(upload_to="post_images/", blank=True, null=True)
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
    description = models.TextField(blank=True, null=True) 
    target_amount = models.DecimalField(max_digits=10, decimal_places=2)
    amount_donated = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        
    
    def save(self, *args, **kwargs):

        self.is_active = self.amount_donated < self.target_amount
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.title} - {self.patient.username}"

    
class DonationPayment(models.Model):
    donation = models.ForeignKey(Donation, on_delete=models.CASCADE, related_name='payments')
    supporter = models.ForeignKey(User, on_delete=models.CASCADE, related_name='donations_made')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    
    

    def clean(self):
        if self.donation.patient_id == self.supporter_id:
            raise ValidationError("Patients cannot donate to their own campaigns.")

        if self.donation.amount_donated + self.amount > self.donation.target_amount:
            raise ValidationError("Donation exceeds the campaign target amount.")

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

        total = self.donation.payments.aggregate(total=Sum("amount"))["total"] or 0
        donation = self.donation
        donation.amount_donated = total
        donation.is_active = total < donation.target_amount
        donation.save(update_fields=["amount_donated", "is_active"])

    def __str__(self):
        return f"{self.supporter.username} donated {self.amount} to {self.donation.title}"
