# urls.py
from django.urls import path
from .views import contact_us, messages_user, all_messages , add_reply, my_replies, delete_message
urlpatterns = [
    path('contact/', contact_us, name='contact'),
    path('contact/messagex`s/', messages_user, name='messages_user'),
    path('contact/all_messages/', all_messages, name='all_messages'),  # Add this line
    path('messages/reply/<int:message_id>/', add_reply, name='add_reply'),  # Add a reply
    path('my_replies/', my_replies, name='replies'),  # Add this line
    path('messages/delete/<int:message_id>/', delete_message, name='delete_message'),  # Add this line


]
