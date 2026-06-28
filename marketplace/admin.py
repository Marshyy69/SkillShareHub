from django.contrib import admin
from .models import FreelanceGig, Order, Profile


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'role')
    list_filter = ('role',)
    search_fields = ('user__username',)


@admin.register(FreelanceGig)
class FreelanceGigAdmin(admin.ModelAdmin):
    list_display = ('title', 'seller', 'category', 'price', 'delivery_time_days', 'created_at')
    list_filter = ('category', 'created_at')
    search_fields = ('title', 'description')


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'gig', 'buyer', 'status', 'date_ordered')
    list_filter = ('status', 'date_ordered')
    search_fields = ('gig__title', 'buyer__username')
