from django.urls import path
from . import views

app_name = 'bank'

urlpatterns = [
    path('', views.account_list, name='bank_data'),
    path('create_account', views.create_account, name='account_create_view'),
    path('account/create', views.create_account, name='account_create'),
    path('account/top_up/<str:account_id>', views.top_up_account, name='top_up'),
    path('account/transfer/<str:account_id>', views.transfer_money, name='transfer_view'),
    path('account/transactions/<str:account_id>', views.transactions_list, name='account_transaction'),
]
