# from django.contrib.postgres.fields import JSONField
import json

from django.core.files.storage import default_storage
from django.db import models
from django.utils.functional import cached_property
from django.conf import settings
import magic
from pathlib import Path


class Blog(models.Model):
    PRIVATE = 'private'
    GROUP = 'group'
    SUPERGROUP = 'supergroup'
    CHANNEL = 'channel'

    TYPE_CHOICES = (
        (PRIVATE, PRIVATE),
        (GROUP, GROUP),
        (SUPERGROUP, SUPERGROUP),
        (CHANNEL, CHANNEL),
    )

    time_created = models.DateTimeField(auto_now_add=True, db_index=True)
    telegram_chat_id = models.BigIntegerField()
    title = models.CharField(blank=True, max_length=300)
    type = models.CharField(choices=TYPE_CHOICES, max_length=20, default=PRIVATE)
    description = models.TextField(blank=True)
    telegram_small_photo_id = models.CharField(max_length=300, blank=True)
    telegram_big_photo_id = models.CharField(max_length=300, blank=True)
    extension = models.CharField(blank=True, max_length=100)

    class Meta:
        verbose_name = 'Blog'
        verbose_name_plural = 'Blogs'

    def __str__(self):
        return self.title

    def media_path(self, file_id):
        return f"telegram_blog/{self.telegram_chat_id}/{file_id}.{self.extension}"

    def file_url(self, file_id):
        media_url = getattr(settings, 'MEDIA_URL')
        path = self.media_path(file_id)
        return media_url + path

    def store_media(self, file_id):
        from .telegram import get_telegram_file_content
        content = get_telegram_file_content(file_id)
        extension = magic.from_buffer(content.read(), mime=True).split('/')[-1]
        content.seek(0)
        self.extension = extension
        # self.save() is called in update_from_chat
        path = self.media_path(file_id)
        default_storage.save(path, content)

    def update_from_chat(self):
        from telegram_blog.utils import request
        data = request('getChat', {'chat_id': self.telegram_chat_id}).get('result')
        if 'description' in data:
            self.description = data['description']
        if 'photo' in data:
            self.telegram_big_photo_id = data['photo']['big_file_id']
            self.telegram_small_photo_id = data['photo']['small_file_id']
            self.store_media(self.telegram_small_photo_id)
            self.store_media(self.telegram_big_photo_id)
        self.save()

    @cached_property
    def photo_url_small(self):
        if not self.telegram_small_photo_id:
            return ''
        return self.file_url(self.telegram_small_photo_id)

    @cached_property
    def photo_url_big(self):
        if not self.telegram_big_photo_id:
            return ''
        return self.file_url(self.telegram_big_photo_id)

    @cached_property
    def last_updated(self):
        most_recent_message = self.entries.order_by('-message_time').first()
        if most_recent_message is None:
            return None
        return most_recent_message.message_time


class Entry(models.Model):
    TEXT = 'text'
    AUDIO = 'audio'
    DOCUMENT = 'document'
    VIDEO = 'video'
    VOICE = 'voice'
    ANIMATION = 'animation'
    PHOTO = 'photo'
    STICKER = 'sticker'
    VIDEO_NOTE = 'video_note'
    CONTACT = 'contact'
    LOCATION = 'location'
    VENUE = 'venue'

    TYPE_CHOICES = (
        (VIDEO, VIDEO),
        (VOICE, VOICE),
        (PHOTO, PHOTO),
        (DOCUMENT, DOCUMENT),
        (AUDIO, AUDIO),
        (ANIMATION, ANIMATION),
        (STICKER, STICKER),
        (VIDEO_NOTE, VIDEO_NOTE),
        (CONTACT, CONTACT),
        (LOCATION, LOCATION),
        (VENUE, VENUE),
        (TEXT, TEXT),  # must be last
    )

    time_created = models.DateTimeField(auto_now_add=True)
    telegram_message_id = models.BigIntegerField(db_index=True)
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE, related_name='entries')
    message_json = models.TextField()
    type = models.CharField(choices=TYPE_CHOICES, max_length=30, default=TEXT)
    message_time = models.DateTimeField(db_index=True)
    edited = models.BooleanField(default=False)
    extension = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return f'{self.blog_id} {self.telegram_message_id}'

    class Meta:
        verbose_name = 'Entry'
        verbose_name_plural = 'Entries'

    @cached_property
    def message(self):
        return json.loads(self.message_json)

    @cached_property
    def template(self):
        return f'telegram_blog/entry_{self.type}.html'

    def media_path(self, file_id):
        return f"telegram_blog/{self.blog.telegram_chat_id}/{file_id}"

    def store_media(self, file_id, extension=None, save_extension=True):
        from .telegram import get_telegram_file_content
        content = get_telegram_file_content(file_id)
        if extension is None:
            extension = magic.from_buffer(content.read(), mime=True).split('/')[-1]
            content.seek(0)
        if extension and save_extension and not self.extension:
            self.extension = extension
            self.save()
        path = self.media_path(file_id) + '.' + extension
        default_storage.save(path, content)

    @cached_property
    def photo_url_display(self):
        if self.type != Entry.PHOTO:
            return ''
        ix = -1
        file_id = None
        # select first image with width <= 800
        for _ in range(5):
            photo = self.message['photo'][ix]
            if photo['width'] <= 800:
                file_id = photo['file_id']
                break
            ix -= 1
        if not file_id:
            return ''
        return self.file_url(file_id)

    @cached_property
    def file_ids(self):
        if self.type == Entry.PHOTO:
            return [x['file_id'] for x in self.message['photo']]
        elif self.type in (Entry.AUDIO,
                           Entry.VOICE,
                           Entry.DOCUMENT,
                           Entry.STICKER,):
            return [self.message[self.type]['file_id']]
        elif self.type in (Entry.VIDEO_NOTE, Entry.VIDEO):
            return [
                self.message[self.type]['file_id'],
                self.message[self.type]['thumb']['file_id'],
            ]
        return []

    @cached_property
    def photo_url_largest(self):
        if self.type != Entry.PHOTO:
            return ''
        file_id = self.message['photo'][-1]['file_id']
        return self.file_url(file_id)

    def file_url(self, file_id=None, extension=None):

        if file_id is None:
            if self.type not in (
                    Entry.AUDIO,
                    Entry.VIDEO_NOTE,
                    Entry.VIDEO,
                    Entry.VOICE,
                    Entry.DOCUMENT,
                    Entry.STICKER):
                return ''

            file_id = self.message[self.type]['file_id']
        media_url = getattr(settings, 'MEDIA_URL')
        path = self.media_path(file_id)
        if extension is None:
            extension = self.extension
        if extension:
            path += f'.{extension}'
        return media_url + path

    @cached_property
    def video_thumb_url(self):
        if self.type not in (Entry.VIDEO, Entry.VIDEO_NOTE):
            return ''
        if 'thumb' not in self.message[self.type]:
            return ''
        file_id = self.message[self.type]['thumb']['file_id']
        return self.file_url(file_id, 'jpeg')

    def store_media_files(self):
        if self.type == Entry.PHOTO:
            for photo_size in self.message['photo']:
                file_id = photo_size['file_id']
                self.store_media(file_id)
        if self.type == Entry.AUDIO:
            self.store_media(self.message['audio']['file_id'])
        if self.type == Entry.VIDEO:
            self.store_media(self.message['video']['file_id'])
            if 'thumb' in self.message['video']:
                self.store_media(self.message['video']['thumb']['file_id'], extension='jpeg', save_extension=False)
        if self.type == Entry.VIDEO_NOTE:
            self.store_media(self.message['video_note']['file_id'])
            if 'thumb' in self.message['video_note']:
                self.store_media(self.message['video_note']['thumb']['file_id'], extension='jpeg', save_extension=False)
        if self.type == Entry.VOICE:
            self.store_media(self.message['voice']['file_id'])
        if self.type == Entry.DOCUMENT:
            file_name = self.message['document'].get('file_name')
            extension = "".join(Path(file_name).suffixes).lstrip(".")
            self.store_media(self.message['document']['file_id'], extension)
        if self.type == Entry.STICKER:
            self.store_media(self.message['sticker']['file_id'])
