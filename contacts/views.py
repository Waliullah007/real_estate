from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.mail import send_mail
from .models import Contact

def contact(request):
    if request.method == 'POST':
        listing_id = request.POST['listing_id']
        listing = request.POST['listing']
        name = request.POST['name']
        email = request.POST['email']
        phone = request.POST['phone']
        message = request.POST['message']
        user_id = request.POST['user_id']
        realtor_email = request.POST['realtor_email']

        # Check if user has made inquiry already
        if request.user.is_authenticated:
            user_id = request.user.id
            has_contacted = Contact.objects.all().filter(listing_id=listing_id, user_id=user_id)
            if has_contacted:
                messages.error(request, 'You have already made an inquiry for this listing')
                return redirect('/listings/' + listing_id)

        contact = Contact(listing=listing, listing_id=listing_id, name=name, email=email, phone=phone, message=message, user_id=user_id)
        contact.save()

        # Send email to realtor
        send_mail(
            'Property Listing Inquiry',
            f'There has been an inquiry for {listing}. Sign into the admin panel for more info.',
            'your_email@example.com',
            [realtor_email, 'another_email@example.com'],
            fail_silently=False
        )

        # Send response email to user
        send_mail(
            'Thank you for your inquiry',
            f'Dear {name},\n\nThank you for your inquiry about {listing}. We have received your message and will get back to you soon.\n\nBest regards,\nYour Company Name',
            'your_email@example.com',
            [email],
            fail_silently=False
        )

        messages.success(request, 'Your request has been submitted, a realtor will get back to you soon')
        return redirect('/listings/' + listing_id)
    

    # views.py
from django.shortcuts import render, get_object_or_404
from .models import Contact, Message

def user_dashboard(request):
    user_contacts = Contact.objects.filter(user_id=request.user.id).prefetch_related('messages')
    return render(request, 'dashboard.html', {'contacts': user_contacts})

def contact_messages(request, contact_id):
    contact = get_object_or_404(Contact, id=contact_id)
    messages = contact.messages.all()
    return render(request, 'contact_messages.html', {'contact': contact, 'messages': messages})



def user_dashboard(request):
    user_contacts = Contact.objects.filter(user_id=request.user.id).prefetch_related('messages')

    if request.method == 'POST':
        contact_id = request.POST.get('contact_id')
        message_text = request.POST.get('message_text')
        if contact_id and message_text:
            contact = get_object_or_404(Contact, id=contact_id, user_id=request.user.id)
            Message.objects.create(contact=contact, user=request.user, text=message_text)
            messages.success(request, 'Message sent successfully')
        return redirect('user_dashboard')

    return render(request, 'dashboard.html', {'contacts': user_contacts})
