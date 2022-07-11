import django.db.utils
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from .models import Category, CategoryForm


@login_required(redirect_field_name='login_account')
def register_category(request):
    if request.method == 'GET':
        form = CategoryForm()
        return render(request, 'category/register_category.html', {'form': form})
    elif request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, f'Category [{request.POST.get("name")}] successfully registered!')
            return redirect('view_category')
        else:
            messages.error(request, 'Error: Could not register Category!')
            return render(request, 'category/register_category.html', {'form': form})


@login_required(redirect_field_name='login_account')
def view_category(request):
    if request.method == 'GET':
        categories = Category.objects.filter()
        total_categories_found = len(categories)
        paginator = Paginator(categories, 5)
        page_number = request.GET.get('page')
        page_object = paginator.get_page(page_number)

        category_object = {
            'categories': page_object,
            'total_categories_found': total_categories_found
        }

        return render(request, 'category/view_category.html', category_object)


@login_required(redirect_field_name='login_account')
def detail_category(request, category_id):
    if request.method == 'GET':
        category = get_object_or_404(Category, id=category_id)
        return render(request, 'category/detail_category.html', {'category': category})


@login_required(redirect_field_name='login_account')
def remove_category(request, category_id):
    category = Category.objects.get(id=category_id)

    try:
        category.delete()
    except django.db.utils.IntegrityError as e:
        messages.error(request, f'Error: Could not remove Category [{category.name}], '
                                f'because it is being used by Contact!')
    else:
        messages.success(request, f'Category [{category.name}] has been removed!')
    finally:
        return redirect('view_category')


@login_required(redirect_field_name='login_account')
def search_category(request):
    if request.method == 'GET':
        search = request.GET.get('search')

        if search is None:
            messages.error(request, 'Error: Invalid search parameters')
            return redirect('view_category')
        elif not search:
            messages.info(request, 'Search field is empty!')
        else:
            messages.info(request, 'Search successfully realized!')

        categories = Category.objects.filter(name__icontains=search)
        total_categories_found = len(categories)

        paginator = Paginator(categories, 10)
        page_number = request.GET.get('page')
        page_object = paginator.get_page(page_number)

        category_object = {
            'categories': page_object,
            'total_categories_found': total_categories_found
        }

        return render(request, 'category/view_category.html', category_object)
