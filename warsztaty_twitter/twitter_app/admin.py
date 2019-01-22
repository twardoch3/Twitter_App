from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Comment, Message, Tweet, User


admin.site.register(User, UserAdmin)

def text_20(obj):
    return obj.content[:30] + '...'

def number_of_comments(obj):
    return obj.comment_set.all().count()


def text_disable(model_admin, request, query_set):
    query_set.update(disabled=True)


text_disable.short_description = 'disable text'


def text_enable(model_admin, request, query_set):
    query_set.update(disabled=False)


text_enable.short_description = 'enable text'


@admin.register(Tweet)
class TweetAdmin(admin.ModelAdmin):
    list_display = [text_20, 'creation_date', 'user', 'disabled', number_of_comments]
    actions = [text_disable, text_enable]


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = [text_20, 'creation_date', 'user', 'tweet', 'disabled']
    actions = [text_disable, text_enable]


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = [text_20, 'creation_date', 'sender', 'receiver', 'read', 'disabled']
    actions = [text_disable, text_enable]



