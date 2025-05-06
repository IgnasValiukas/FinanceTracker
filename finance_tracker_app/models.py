from django.db import models
from django.db.models import TextField
from django.contrib.auth.models import User


class Category(models.Model):
    name = models.CharField('Category Name', max_length=200, help_text='Add category', unique=True)

    def __str__(self):
        return self.name


class Transaction(models.Model):
    TYPE_CHOICES = [
        ('i', 'Income'),
        ('e', 'Expense')
    ]
    amount = models.DecimalField('Amount of money', help_text='Add amount of money', blank=False, null=False,
                                 default=0.0, max_digits=12, decimal_places=2)
    type = models.CharField(max_length=1, choices=TYPE_CHOICES, default='e')
    title = models.CharField(max_length=200, blank=False, help_text='Add transaction title')
    category = models.ForeignKey('Category', on_delete=models.SET_NULL, null=True, blank=False)
    date = models.DateField(help_text='Add transaction date')
    description = TextField(max_length=2000, blank=True, help_text='Write description (optional)')
    account = models.ForeignKey('Account', on_delete=models.CASCADE, null=True)

    def __str__(self):
        return f'{self.account.profile.user}: {self.amount}, {self.type}, {self.title}, {self.category}, {self.date}'


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default="profile_pics/default_profile.png")

    def __str__(self):
        return f'{self.user}'

    # later add logic


class Account(models.Model):
    profile = models.OneToOneField('Profile', on_delete=models.SET_NULL, null=True, blank=False)
    balance = models.DecimalField('Account balance', blank=False, null=False, default=0.0, max_digits=12,
                                  decimal_places=2)

    def __str__(self):
        return f'{self.profile.user}'
