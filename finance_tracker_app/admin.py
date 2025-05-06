from django.contrib import admin
from .models import Category, Transaction, Profile, Account

admin.site.register(Category)
admin.site.register(Transaction)
admin.site.register(Profile)
admin.site.register(Account)
