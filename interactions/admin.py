from django.contrib import admin
from .models import Like, Comment, Follow, Conversation, ConversationMessage

admin.site.register(Like)
admin.site.register(Comment)
admin.site.register(Follow)
admin.site.register(ConversationMessage)
admin.site.register(Conversation)
