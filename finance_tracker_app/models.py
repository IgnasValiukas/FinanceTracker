from django.core.exceptions import ValidationError
from tinymce.models import HTMLField
from django.db import models
from django.db.models import TextField
from django.contrib.auth.models import User


class Category(models.Model):
    TYPE_CHOICES = [
        ('i', 'Income'),
        ('e', 'Expense'),
        ('b', 'Both'),
    ]

    name = models.CharField('Category Name', max_length=200, help_text='Add category')
    category_type = models.CharField(max_length=1, choices=TYPE_CHOICES, default='b')

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'
        constraints = [
            models.UniqueConstraint(fields=['name', 'category_type'], name='unique_category_type')
        ]


class Transaction(models.Model):
    TYPE_CHOICES = [
        ('i', 'Income'),
        ('e', 'Expense'),
    ]

    amount = models.DecimalField('Amount of money', help_text='Add amount of money', blank=False, null=False,
                                 default=0.0, max_digits=12, decimal_places=2)
    type = models.CharField(max_length=1, choices=TYPE_CHOICES, default='e')
    title = models.CharField(max_length=200, blank=False, help_text='Add transaction title')
    category = models.ForeignKey('Category', on_delete=models.SET_NULL, null=True, blank=False)
    date = models.DateField(help_text='Add transaction date')
    description = HTMLField(blank=True, null=True)
    client = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def clean(self):
        super().clean()
        if self.category:
            cat_type = self.category.category_type
            if cat_type != 'b' and cat_type != self.type:
                raise ValidationError({
                    'category': f"Category '{self.category.name}' is not valid for transaction type '{self.get_type_display()}'."
                })

    def __str__(self):
        return f'{self.client}: {self.amount}€ - {self.category.name}, {self.get_type_display()} ({self.date})'

    class Meta:
        verbose_name = 'Transaction'
        verbose_name_plural = 'Transactions'


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default="profile_pics/default_profile.png")

    def __str__(self):
        return f'{self.user.username}'

    class Meta:
        verbose_name = 'Profile'
        verbose_name_plural = 'Profiles'

    # later add logic
