# contact/views.py

from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import ContactMessageForm

# View to display the Contact Us form and handle form submissions
def contact_us(request):
    if request.method == 'POST':
        form = ContactMessageForm(request.POST)
        if form.is_valid():
            form.save()  # Save the message to the database
            messages.success(request, 'Your message has been sent successfully.')
            return redirect('contact:contact_us')  # Redirect to the same page or another page after submission
        else:
            messages.error(request, 'Failed to send your message. Please correct the errors below.')
    else:
        form = ContactMessageForm()
    return render(request, 'contact/contact_us.html', {'form': form})
