from django.http import HttpResponse
from .models import Transaction, Category
from .forms import UserUpdateForm, ProfileUpdateForm, TransactionForm
from django.db.models import Sum
from django.contrib import messages
from django.contrib.messages import get_messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import User
from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.core.paginator import Paginator
from django.views.decorators.csrf import csrf_protect
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
)


def index(request):
    return render(request, 'index.html')


def about(request):
    return render(request, 'about.html')


@login_required
def search(request):
    query = request.GET.get('query')
    user = request.user
    search_results = Transaction.objects.filter(client=user, title__icontains=query)
    return render(request, 'search.html', {'transactions': search_results, 'query': query})


class TransactionsByUserListView(LoginRequiredMixin, ListView):
    model = Transaction
    context_object_name = 'transactions'
    template_name = 'user_transactions.html'
    paginate_by = 12

    def get_queryset(self):
        return Transaction.objects.filter(client=self.request.user).order_by('-date')


class TransactionByUserDetailView(LoginRequiredMixin, DetailView):
    model = Transaction
    template_name = 'user_transaction.html'
    context_object_name = 'transaction'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        transaction = self.get_object()

        transactions_qs = Transaction.objects.filter(category=transaction.category, client=self.request.user).order_by(
            '-date')

        paginator = Paginator(transactions_qs, 3)
        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        context['transaction_set'] = page_obj
        return context


class TransactionByUserCreateView(LoginRequiredMixin, CreateView):
    model = Transaction
    form_class = TransactionForm
    success_url = "/finance/mytransactions/"
    template_name = 'user_transaction_form.html'

    def form_valid(self, form):
        form.instance.client = self.request.user
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_edit'] = False
        return context


class TransactionByUserUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Transaction
    form_class = TransactionForm
    success_url = "/finance/mytransactions/"
    template_name = 'user_transaction_form.html'

    def form_valid(self, form):
        form.instance.client = self.request.user
        return super().form_valid(form)

    def test_func(self):
        transaction = self.get_object()
        return self.request.user == transaction.client

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_edit'] = True
        return context


class TransactionByUserDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Transaction
    success_url = "/finance/mytransactions/"
    template_name = 'user_transaction_delete.html'

    def test_func(self):
        transaction = self.get_object()
        return self.request.user == transaction.client


@login_required
def dashboard(request):
    return render(request, 'user_dashboard.html')


@csrf_protect
def register(request):
    list(get_messages(request))
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
    user = request.user
    if request.method == "POST":
        user_form = UserUpdateForm(request.POST, instance=user)
        profile_form = ProfileUpdateForm(request.POST, request.FILES, instance=user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, "Profile updated!")
            return redirect('profile')
    else:
        user_form = UserUpdateForm(instance=user)
        profile_form = ProfileUpdateForm(instance=user.profile)

    transactions = Transaction.objects.filter(client=user)

    transaction_count = transactions.count()
    total_income = transactions.filter(type='i').aggregate(total=Sum('amount'))['total'] or 0
    total_expenses = transactions.filter(type='e').aggregate(total=Sum('amount'))['total'] or 0
    balance = total_income - total_expenses

    context = {
        'user_form': user_form,
        'profile_form': profile_form,
        'transaction_count': transaction_count,
        'total_income': round(total_income, 2),
        'total_expenses': round(total_expenses, 2),
        'balance': round(balance, 2)
    }
    return render(request, 'profile.html', context)
