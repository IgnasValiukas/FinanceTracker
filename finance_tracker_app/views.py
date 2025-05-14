from django.http import HttpResponse
from .models import Transaction, Category
from .forms import UserUpdateForm, ProfileUpdateForm
from django.db.models import Q
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import User
from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.core.paginator import Paginator
from django.views import generic
from django.views.decorators.csrf import csrf_protect
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


class TransactionsByUserListView(LoginRequiredMixin, ListView):
    model = Transaction
    context_object_name = 'transactions'
    template_name = 'user_transactions.html'
    paginate_by = 15

    def get_queryset(self):
        return Transaction.objects.filter(client=self.request.user)


class TransactionByUserDetailView(LoginRequiredMixin, DetailView):
    model = Transaction
    template_name = 'user_transaction.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        transaction = self.get_object()
        context['transaction_set'] = Transaction.objects.filter(category=transaction.category, client=self.request.user)
        return context


class TransactionByUserCreateView(LoginRequiredMixin, CreateView):
    model = Transaction
    fields = ['amount', 'type', 'title', 'category', 'date', 'description']
    success_url = "/finance/mytransactions/"
    template_name = 'user_transaction_form.html'

    def form_valid(self, form):
        form.instance.client = self.request.user
        return super().form_valid(form)


class TransactionByUserUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Transaction
    fields = ['amount', 'type', 'title', 'category', 'date', 'description']
    success_url = "/finance/mytransactions/"
    template_name = 'user_transaction_form.html'

    def form_valid(self, form):
        form.instance.client = self.request.user
        return super().form_valid(form)

    def test_func(self):
        transaction = self.get_object()
        return self.request.user == transaction.client


class TransactionByUserDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Transaction
    success_url = "/finance/mytransactions/"
    template_name = 'user_transaction_delete.html'

    def test_func(self):
        transaction = self.get_object()
        return self.request.user == transaction.client


@csrf_protect
def register(request):
    if request.method == "POST":
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']
        if password == password2:
            if User.objects.filter(username=username).exists():
                messages.error(request, f'Username \'{username}\' already exists!')
                return redirect('register')
            else:
                if User.objects.filter(email=email).exists():
                    messages.error(request, f'User with email \'{email}\' is already registered!')
                    return redirect('register')
                else:
                    User.objects.create_user(username=username, email=email, password=password)
                    messages.info(request, f'User \'{username}\' successfully registered!')
                    return redirect('login')
        else:
            messages.error(request, 'Passwords do not match!')
            return redirect('register')
    return render(request, 'registration/register.html')


@login_required
def profile(request):
    if request.method == "POST":
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, f"Profile updated!")
            return redirect('profile')
    else:
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=request.user.profile)
    context = {
        'user_form': user_form,
        'profile_form': profile_form,
    }
    return render(request, 'profile.html')
