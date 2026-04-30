from django.contrib import admin
from apps.users.models import Customer, ProfileKYC


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'first_name',
                    'last_name', 'is_active', 'date_joined')
    search_fields = ('username', 'email', 'first_name', 'last_name')
    list_filter = ('is_active', 'is_staff', 'is_superuser')


@admin.register(ProfileKYC)
class ProfileKYCAdmin(admin.ModelAdmin):
    list_display = ('name', 'user_id', 'dob', 'id_card', 'issue_date')
    search_fields = ('name', 'id_card')
