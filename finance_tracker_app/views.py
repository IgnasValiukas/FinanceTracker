from django.http import HttpResponse
from django.db.models import Q
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Transaction, Category
from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.core.paginator import Paginator
from django.views import generic
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
)


def index(request):
    num_categories = Category.objects.all().count()
    num_transactions = Transaction.objects.all().count()

    num_visits = request.session.get('num_visits', 1)
    request.session['num_visits'] = num_visits + 1
    context = {
        'num_categories': num_categories,
        'num_transactions': num_transactions,
        'num_visits': num_visits,
    }
    return render(request, 'index.html', context=context)


class TransactionListView(generic.ListView):
    model = Transaction
    paginate_by = 15
    template_name = 'transaction_list.html'


class TransactionDetailView(generic.DetailView):
    model = Transaction
    template_name = 'transaction_detail.html'

    def get_success_url(self):
        return reverse('transaction-detail', kwargs={'pk': self.object.id})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        transaction = self.get_object()
        context['transaction_set'] = Transaction.objects.filter(category=transaction.category)
        return context


def search(request):
    query = request.GET.get('query')
    search_results = Transaction.objects.filter(Q(title__icontains=query))
    return render(request, 'search.html', {'transactions': search_results, 'query': query})


class TransactionsByUserListView(LoginRequiredMixin, generic.ListView):
    model = Transaction
    template_name = 'user_transactions.html'
    paginate_by = 15

    def get_queryset(self):
        return Transaction.objects.filter(client=self.request.user)
