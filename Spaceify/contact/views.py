# contact/views.py

from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.conf import settings
from django.contrib import messages
from .forms import ContactMessageForm

# View to display the Contact Us form and handle form submissions
def contact_us(request):
    if request.method == 'POST':
        form = ContactMessageForm(request.POST)
        if form.is_valid():
            # Get form data
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            message = form.cleaned_data['message']

            # Send email
            send_mail(
                f"Message from {name} ({email})",
                message,
                email,  # Sender's email
                [settings.DEFAULT_FROM_EMAIL],  # Admin's email or recipient
            )

            messages.success(request, 'Your message has been sent successfully.')
            return redirect('contact:contact_us')
        else:
            messages.error(request, 'Failed to send your message. Please correct the errors below.')
    else:
        form = ContactMessageForm()
    return render(request, 'contact/contact_us.html', {'form': form})
