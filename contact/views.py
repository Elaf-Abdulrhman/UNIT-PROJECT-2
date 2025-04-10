from django.contrib import messages
from django.shortcuts import render, redirect
from .forms import ContactForm

def contact_view(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            # Process the form (e.g., send an email)
            form.save()  # Or handle the form data as needed
            messages.success(request, 'Your message has been sent. Thank you!')
            return redirect('contact')  # Redirect to avoid resubmission
        else:
            messages.error(request, 'There was an error sending your message. Please try again.')
    else:
        form = ContactForm()

    return render(request, 'contact/contact.html', {'form': form})
