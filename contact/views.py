from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.core.paginator import Paginator
from django.core.validators import validate_email
from .models import Contact, ContactForm


def view_contact(request):
    if request.method == 'GET':
        contacts = Contact.objects.all()
        total_contacts_found = len(contacts)
        paginator = Paginator(contacts, 10)
        page_number = request.GET.get('page')
        page_object = paginator.get_page(page_number)

        contact_object = {
            'contacts': page_object,
            'total_contacts_found': total_contacts_found
        }

        return render(request, 'contact/view_contact.html', contact_object)


def detail_contact(request, contact_id):
    if request.method == 'GET':
        contact = get_object_or_404(Contact, id=contact_id)
        return render(request, 'contact/detail_contact.html', {'contact': contact})


def remove_contact(request, contact_id):
    contact = get_object_or_404(Contact, id=contact_id)
    contact.delete()
    messages.success(request, f'Contact [{contact.name}] has been removed')
    return redirect('view_contact')


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
