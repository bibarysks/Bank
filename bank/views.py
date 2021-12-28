import uuid
from django.shortcuts import render, redirect
from django.db import connection
from datetime import datetime


def dictfetchall(cursor):
    desc = cursor.description
    return [
        dict(zip([col[0] for col in desc], row))
        for row in cursor.fetchall()
    ]


def dictfetchone(cursor):
    res = dictfetchall(cursor)
    return res[0]


def account_list(request):
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM account")
    r = dictfetchall(cursor)

    print(connection.queries)

    return render(request, 'home.html', {'data': r})


def create_account(request):
    if request.method == 'POST':
        if request.POST['currency'] in ['KZT', 'USD', 'RUB']:
            with connection.cursor() as cursor:
                cursor.execute("insert into account(id, balance, currency) values(%s, %s, %s)",
                               [str(uuid.uuid4()), 0, request.POST['currency']])
            return redirect('/')
        else:
            return render(request, 'create_account.html', {'error': True})
    else:
        return render(request, 'create_account.html', {'error': False})


def top_up_account(request, account_id):
    if request.method == 'POST':
        with connection.cursor() as cursor:
            cursor.execute("select * from account where id = %s", [account_id])
            account = dictfetchone(cursor)
            update_balance(cursor, account_id, account_id, account_id, account['balance'], int(request.POST['amount']))
        return redirect('/account/transactions/' + account_id)
    else:
        return render(request, 'topup_balance.html', {'id': account_id})


def transactions_list(request, account_id):
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM transfer where account_id = %s order by date_time desc", [account_id])
        r = dictfetchall(cursor)
        cursor.execute("select * from account where id = %s", [account_id])
        account = dictfetchone(cursor)
        return render(request, 'transactions.html', {'account': account, 'transactions': r})


def update_balance(cursor, id, from_id, to_id, balance, amount):
    if to_id == id:
        new_balance = balance + amount
    else:
        new_balance = balance - amount
    cursor.execute("update account set balance = %s where id = %s", [new_balance, id])
    cursor.execute(
        "insert into transfer(id, account_id, balance, amount, from_account, to_account, date_time) values(%s, %s, %s,"
        " %s, %s, %s, %s)",
        [str(uuid.uuid4()), id, new_balance, amount, from_id, to_id, str(datetime.now())])


def transfer_money(request, account_id):
    with connection.cursor() as cursor:
        cursor.execute("select * from account where id = %s", [account_id])
        account = dictfetchone(cursor)
        cursor.execute("select * from account where currency = %s and id <> %s", [account['currency'], account_id])
        accounts = dictfetchall(cursor)
        if request.method == 'POST':
            amount = int(request.POST['amount'])
            if account['balance'] >= amount:
                update_balance(cursor, account_id, account_id, request.POST['account'], account['balance'], amount)
                cursor.execute("select * from account where id = %s", [request.POST['account']])
                to_account = dictfetchone(cursor)
                update_balance(cursor, request.POST['account'], account_id, request.POST['account'],
                               to_account['balance'], amount)
                return redirect('/account/transactions/' + account_id)
            else:
                return render(request, 'transfer.html', {'account': account, 'accounts': accounts, 'error': True})
        else:
            return render(request, 'transfer.html', {'account': account, 'accounts': accounts, 'error': False})
