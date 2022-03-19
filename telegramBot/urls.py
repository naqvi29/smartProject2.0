from unicodedata import name
from django.urls import path

from . import views

urlpatterns = [
    path('user-dashboard', views.user_dashboard, name='user-dashboard'),
    path('user-profile', views.user_profile, name='user_profile'),
    path('telegram-dm-bot', views.telegram_dm_bot, name='telegram_dm_bot'),
    # path('telegram-bot-send/<str:category>/<int:id>/<str:sent>', views.telegram_bot_send, name='telegram_bot_send'),
    path('telegram-dmBot-send/<int:id>/<str:sent>', views.telegram_dmBot_send, name='telegram_dmBot_send'),
    path('send-chat/<int:id>', views.send_chat, name='send_chat'),
    path('send-answer/<int:id>', views.send_answer, name='send_answer'),
    path('telegram-bot-add-group/<str:category>', views.telegram_bot_add_group, name='telegram_bot_add_group'),
    path('telegram-bot-add-question', views.telegram_bot_add_question, name='telegram_bot_add_question'),
    path('telegram-bot-add-answer', views.telegram_bot_add_answer, name='telegram_bot_add_answer'),
    path('delete-telegram-account/<int:id>', views.delete_telegram_account, name='delete_telegram_account'),
    path('edit-telegram-account/<int:id>', views.edit_telegram_account, name='edit_telegram_account'),
    path('telegram-bot-add-question', views.telegram_bot_add_question, name='telegram_bot_add_question'),
    path('delete-telegram-groups/<int:id>', views.delete_telegram_groups, name='delete_telegram_groups'),
    path('delete-telegram-questions/<int:id>', views.delete_telegram_questions, name='delete_telegram_questions'),
    path('delete-telegram-answers/<int:id>', views.delete_telegram_answers, name='delete_telegram_answers'),
    path('coming-soon', views.coming_soon, name='coming_soon'),
    path('schedule-messages', views.schedule_messages, name='schedule_messages'),
    path('delete-schedule-messages/<int:id>', views.delete_schedule_messages, name='delete_schedule_messages'),
    path('time-now', views.time_now, name='time_now'),
]