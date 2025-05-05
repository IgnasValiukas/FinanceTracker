from django.db import models
from django.db.models import TextField
from django.contrib.auth.models import User


class Category(models.Model):
    name = models.CharField('Category Name', max_length=200, help_text='Add category')


class Type(models.Model):
    TRANSACTION_STATUS = (
        ('i', 'income'),
        ('e', 'expense')
    )

    status = models.CharField(
        max_length=1,
        choices=TRANSACTION_STATUS,
        default='e',
        help_text='Transaction Status'
    )


class Transaction(models.Model):
    amount = models.DecimalField('Amount of money', help_text='Add amount of money', blank=False, null=False)
    type_id = models.ForeignKey('Type', on_delete=models.SET_NULL, null=True, blank=False)
    title = models.CharField(max_length=200, blank=False, help_text='Add transaction title')
    category_id = models.ForeignKey('Category', on_delete=models.SET_NULL, null=True, blank=False)
    date = models.DateTimeField(help_text='Add transaction date')
    description = TextField(max_length=2000)


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField()

    # later add logic


class Account(models.Model):
    profile_id = models.ForeignKey('Profile', on_delete=models.SET_NULL, null=True, blank=False)
    balance = models.DecimalField('Account balance')
    transaction_id = models.ForeignKey('Transaction', on_delete=models.SET_NULL, null=True, blank=False)
