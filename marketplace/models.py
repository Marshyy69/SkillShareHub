from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    ROLE_CHOICES = [
        ('buyer', 'Buyer'),
        ('seller', 'Seller'),
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='buyer')

    def __str__(self):
        return f'{self.user.username} ({self.get_role_display()})'


class FreelanceGig(models.Model):
    CATEGORY_CHOICES = [
        ('tech', 'Graphics & Design'),
        ('prog', 'Programming & Tech'),
        ('writing', 'Writing & Translation'),
        ('video', 'Video & Animation'),
    ]
    title = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    delivery_time_days = models.IntegerField(default=3)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name='gigs')
    image = models.ImageField(upload_to='gig_images/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('progress', 'In Progress'),
        ('delivered', 'Delivered'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]
    gig = models.ForeignKey(FreelanceGig, on_delete=models.CASCADE, related_name='orders')
    buyer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='purchases')
    requirements = models.TextField(blank=True, help_text='Describe your project, ideas, and what you need.')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    date_ordered = models.DateTimeField(auto_now_add=True)
    
    # Submission fields
    submission_text = models.TextField(blank=True, help_text="Submission message or links (e.g. Google Drive, GitHub)")
    submission_file = models.FileField(upload_to='submissions/', blank=True, null=True, help_text="Upload completed file")
    date_submitted = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return f'Order #{self.id} - {self.gig.title}'
