from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.core.paginator import Paginator
from django.core.validators import validate_email
from django.db.models import Q, Value
from django.db.models.functions import Concat
from django.contrib.auth.decorators import login_required
from .models import Contact, ContactForm


@login_required(redirect_field_name='login_account')
def view_contact(request):
    if request.method == 'GET':
        contacts = Contact.objects.all()
        total_contacts_found = len(contacts)
        paginator = Paginator(contacts, 5)
        page_number = request.GET.get('page')
        page_object = paginator.get_page(page_number)

        contact_object = {
            'contacts': page_object,
            'total_contacts_found': total_contacts_found
        }

        return render(request, 'contact/view_contact.html', contact_object)


@login_required(redirect_field_name='login_account')
def detail_contact(request, contact_id):
    if request.method == 'GET':
        contact = get_object_or_404(Contact, id=contact_id)
        return render(request, 'contact/detail_contact.html', {'contact': contact})


@login_required(redirect_field_name='login_account')
def remove_contact(request, contact_id):
    contact = get_object_or_404(Contact, id=contact_id)
    contact.delete()
    messages.success(request, f'Contact [{contact.name}] has been removed')
    return redirect('view_contact')


@login_required(redirect_field_name='login_account')
def register_contact(request):
    if request.method == 'GET':
        form = ContactForm()
        return render(request, 'contact/register_contact.html', {'form': form})
    elif request.method == 'POST':
        form = ContactForm(request.POST, request.FILES)
        phone = request.POST.get('phone')
        name = request.POST.get('name')
        email = request.POST.get('email')

        if not form.is_valid() or not phone.isnumeric() or len(name) < 4:
            messages.error(request, f'Error: Phone must be numeric and Name must have at least 4 characters')
        else:
            try:
                if email:
                    validate_email(email)
            except:
                messages.error(request, f'Error: Email is invalid')
            else:
                form.save()
                messages.success(request, f'Contact {request.POST.get("name")} has been added!')
                return redirect('view_contact')

        return render(request, 'contact/register_contact.html', {'form': form})


@login_required(redirect_field_name='login_account')
def search_contact(request):
    if request.method == 'GET':
        search = request.GET.get('search')

        if search is None:
            messages.error(request, 'Invalid search parameters')
            redirect('view_contact')
        elif not search:
            messages.info(request, 'Search field is empty!')
        else:
            messages.info(request, 'Search successfully realized!')

        search_fields = Concat('name', Value(' '), 'surname')

        contacts = Contact.objects.annotate(
            full_name=search_fields
        ).filter(
            Q(full_name__icontains=search) | Q(phone__icontains=search) | Q(email__icontains=search) |
            Q(phone__icontains=search) | Q(category__name__icontains=search)
        )

        total_contacts_found = len(contacts)

        paginator = Paginator(contacts, 10)
        page_number = request.GET.get('page')
        page_object = paginator.get_page(page_number)

        contact_object = {
            'contacts': page_object,
            'total_contacts_found': total_contacts_found
        }

        return render(request, 'contact/view_contact.html', contact_object)
