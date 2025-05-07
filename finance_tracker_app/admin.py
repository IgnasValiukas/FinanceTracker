from django.contrib import admin
from .models import Category, Transaction, Profile


class TransactionAdmin(admin.ModelAdmin):
    list_display = ('amount', 'type', 'title', 'category', 'date', 'description', 'profile')


admin.site.register(Profile)
admin.site.register(Category)
admin.site.register(Transaction)

