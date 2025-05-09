from django.contrib import admin
from .models import Category, Transaction, Profile


class TransactionAdmin(admin.ModelAdmin):
    list_display = ('client', 'amount', 'category', 'timestamp')
    list_filter = ('client', 'timestamp')


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'category_type')
    list_filter = ('category_type',)


admin.site.register(Profile)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Transaction, TransactionAdmin)
