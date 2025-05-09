from django.http import HttpResponse
from .models import Transaction, Category
from django.shortcuts import render


def index(request):
    num_categories = Category.objects.all().count()
    num_transactions = Transaction.objects.all().count()

    context = {
        'num_categories': num_categories,
        'num_transactions': num_transactions,
    }

    return render(request, 'index.html', context=context)
