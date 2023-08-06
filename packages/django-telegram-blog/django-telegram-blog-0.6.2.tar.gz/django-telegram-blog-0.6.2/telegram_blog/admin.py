from django.contrib import admin
from .models import Blog, Entry


class BlogAdmin(admin.ModelAdmin):
    list_display = [
        'title',
        'type',
        'time_created',
    ]

    date_hierarchy = 'time_created'


class EntryAdmin(admin.ModelAdmin):
    list_display = [
        'telegram_message_id',
        'blog_id',
        'type',
        'message_time',
        'edited',
    ]

    date_hierarchy = 'message_time'
    readonly_fields = [
        'telegram_message_id',
        'type',
        'blog',
        'file_ids',
    ]


admin.site.register(Blog, BlogAdmin)
admin.site.register(Entry, EntryAdmin)
