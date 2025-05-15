from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
    path('transactions/', views.TransactionListView.as_view(), name='transactions'),
    path('transactions/<int:pk>', views.TransactionDetailView.as_view(), name='transaction-detail'),
    path('search/', views.search, name='search'),
    path('mytransactions/', views.TransactionsByUserListView.as_view(), name='my-transactions'),
    path('mytransactions/<int:pk>', views.TransactionByUserDetailView.as_view(), name='my-transaction'),
    path('mytransactions/new', views.TransactionByUserCreateView.as_view(), name='my-transaction-new'),
    path('mytransactions/<int:pk>/update', views.TransactionByUserUpdateView.as_view(), name='my-transaction-update'),
    path('mytransactions/<int:pk>/delete', views.TransactionByUserDeleteView.as_view(), name='my-transaction-delete'),
    path('register/', views.register, name='register'),
    path('profile/', views.profile, name='profile'),
]
