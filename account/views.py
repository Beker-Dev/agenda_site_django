from django.shortcuts import render, redirect, get_object_or_404
from django.core.validators import validate_email
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.contrib import auth, messages
from django.db.models import Q, Value
from django.db.models.functions import Concat
from .models import UserForm


def login_account(request):
    if request.method == 'GET':
        if request.user.is_authenticated:
            return redirect('view_contact')
        else:
            return render(request, 'account/login_account.html')
    elif request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        account = auth.authenticate(request, username=username, password=password)

        if account is not None:
            auth.login(request, account)
            return redirect('view_contact')
        else:
            messages.error(request, 'Error: Invalid Username or Password!')
            return render(request, 'account/login_account.html')


@login_required(redirect_field_name='login_account')
def logout_account(request):
    auth.logout(request)
    return redirect('login_account')


@login_required(redirect_field_name='login_account')
def view_account(request):
    if request.method == 'GET':
        accounts = User.objects.all()
        total_accounts_found = len(accounts)
        account_logged_in = request.user.username

        paginator = Paginator(accounts, 10)
        page_number = request.GET.get('page')
        page_object = paginator.get_page(page_number)

        account_object = {
            'account_logged_in': account_logged_in,
            'accounts': page_object,
            'total_accounts_found': total_accounts_found
        }

        return render(request, 'account/view_account.html', account_object)


@login_required(redirect_field_name='login_account')
def detail_account(request, account_id):
    if request.method == 'GET':
        account = get_object_or_404(User, id=account_id)
        return render(request, 'account/detail_account.html', {'account': account})


@login_required(redirect_field_name='login_account')
def remove_account(request, account_id):
    account = get_object_or_404(User, id=account_id)
    account.delete()
    messages.success(request, f'Account [{account.username}] has been removed!')
    return redirect('view_account')


@login_required(redirect_field_name='login_account')
def register_account(request):
    if request.method == 'GET':
        form = UserForm()
        return render(request, 'account/register_account.html', {'form': form})
    elif request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Account has been registered!')
            return redirect('view_account')
        else:
            messages.error(request, 'Account could not be registered!')
            return render(request, 'account/register_account.html', {'form': form})


@login_required(redirect_field_name='login_account')
def search_account(request):
    if request.method == 'GET':
        search = request.GET.get('search')

        if search is None:
            messages.error(request, 'Error: Invalid search parameters!')
            return redirect('view_account')
        elif not search:
            messages.info(request, 'Search field is empty!')
        else:
            messages.info(request, 'Search successfully realized!')

        full_name = Concat('first_name', Value(' '), 'last_name')

        accounts = User.objects.annotate(
            full_name=full_name
        ).filter(
            Q(full_name__icontains=search) | Q(username__icontains=search) | Q(email__icontains=search)
        )

        total_accounts_found = len(accounts)

        paginator = Paginator(accounts, 10)
        page_number = request.GET.get('page')
        page_object = paginator.get_page(page_number)

        account_object = {
            'accounts': page_object,
            'total_accounts_found': total_accounts_found
        }

        return render(request, 'account/view_account.html', account_object)
