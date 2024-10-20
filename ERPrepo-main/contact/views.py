from .forms import ContactForm, ReplyForm
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Message, Reply  # Make sure to import the Reply model
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, get_object_or_404
from .models import Message


@login_required
def delete_message(request, message_id):
    message = get_object_or_404(Message, id=message_id)

    if message.user == request.user:  # Ensure the user can only delete their own messages
        message.delete()

    return redirect('messages_user')  # Redirect to the messages list after deletion


@login_required
def my_replies(request):
    # Get messages sent by the logged-in user and fetch replies
    messages = Message.objects.filter(user=request.user).order_by('-created_at')  # Order by created_at
    message_replies = {message: Reply.objects.filter(message=message).order_by('-created_at') for message in messages}

    return render(request, 'users/replies.html', {'message_replies': message_replies})

@login_required
def all_messages(request):
    messages = Message.objects.all().order_by('-created_at')  # Get all messages ordered by created_at
    reply_form = ReplyForm()  # Initialize an empty reply form
    return render(request, 'users/all_messages.html', {'messages': messages, 'reply_form': reply_form})

@login_required
def add_reply(request, message_id):
    message = get_object_or_404(Message, id=message_id)
    if request.method == 'POST':
        reply_form = ReplyForm(request.POST, request.FILES)  # Include request.FILES for image upload
        if reply_form.is_valid():
            reply = reply_form.save(commit=False)
            reply.user = request.user  # Assign the logged-in user to the reply
            reply.message = message  # Link reply to the specific message
            reply.save()
            return redirect('all_messages')  # Redirect to the message list

    return redirect('all_messages')  # Redirect if the form is invalid or GET request

@login_required
def messages_user(request):
    # Retrieve messages sent by the logged-in user
    messages = Message.objects.filter(user=request.user).order_by('-created_at')  # Order by created_at
    return render(request, 'users/messages.html', {'messages': messages})

def contact_us(request):
    if request.method == 'POST':
        form = ContactForm(request.POST, request.FILES)  # Include request.FILES for image upload
        if form.is_valid():
            content = form.cleaned_data['content']
            message = Message.objects.create(user=request.user, content=content)  # Auto-assign the logged-in user
            if form.cleaned_data['image']:  # Check if an image was uploaded
                message.image = form.cleaned_data['image']
                message.save()
            return redirect('messages_user')  # Redirect to the messages page
    else:
        form = ContactForm()

    return render(request, 'users/contact.html', {'form': form})

def success_view(request):
    return render(request, 'users/success.html')  # Optional, can be removed
