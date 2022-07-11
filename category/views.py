from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import HttpResponse, Http404
from django.core.paginator import Paginator
from .models import Category, CategoryForm


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


def view_category(request):
    if request.method == 'GET':
        categories = Category.objects.filter(is_active=True)
        total_categories_found = len(categories)
        paginator = Paginator(categories, 5)
        page_number = request.GET.get('page')
        print(page_number)
        page_object = paginator.get_page(page_number)

        category_object = {
            'categories': page_object,
            'total_categories_found': total_categories_found
        }

        return render(request, 'category/view_category.html', category_object)


def detail_category(request, category_id):
    if request.method == 'GET':
        category = get_object_or_404(Category, id=category_id, is_active=True)
        return render(request, 'category/detail_category.html', {'category': category})


def remove_category(request, category_id):
    category = Category.objects.get(id=category_id)
    category.is_active = False
    category.save()
    messages.success(request, f'Category [{category.name}] has been removed!')
    return redirect('view_category')
