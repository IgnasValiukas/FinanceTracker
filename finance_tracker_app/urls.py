from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('transactions/', views.TransactionListView.as_view(), name='transactions'),
    path('transactions/<int:pk>', views.TransactionDetailView.as_view(), name='transaction-detail'),
    path('search/', views.search, name='search'),
    path('mytransactions/', views.TransactionsByUserListView.as_view(), name='my-transactions'),
]
