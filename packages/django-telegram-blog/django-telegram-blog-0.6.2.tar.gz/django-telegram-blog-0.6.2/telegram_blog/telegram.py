from telegram_blog.utils import request
from .utils import get_bot_token, session
from .models import Blog, Entry
from datetime import datetime, timezone
import json
import logging
from io import BytesIO

logger = logging.getLogger(__name__)


def get_message_type(message):
    for choice, _ in Entry.TYPE_CHOICES:
        if choice in message:
            return choice


def process_update(update):
    logger.debug("processing update")

    if 'edited_message' in update or 'edited_channel_post' in update:
        edited_message = update.get('edited_message') or update.get('edited_channel_post')
        edited_message_id = edited_message['message_id']
        try:
            existing_entry = Entry.objects.get(
                telegram_message_id=edited_message_id
            )
        except Entry.DoesNotExist:
            logger.warning(f"edited_message with id {edited_message_id} does not exist")
            return
        existing_entry.edited = True
        existing_entry.message_json = json.dumps(edited_message)
        existing_entry.save()
        return

    elif 'message' in update or 'channel_post' in update:
        message = update.get('message') or update.get('channel_post')
        chat, user = message.get('chat'), message.get('from')
        if chat is None:
            logger.info(f'Received update that cannot be processed: {update}')
            return
        chat_id = chat.get('id')
        chat_name = chat.get('username') or chat.get('title') or chat.get('first_name') or chat_id
        blog, created = Blog.objects.get_or_create(
            telegram_chat_id=chat_id,
            defaults={
                'title': chat_name,
                'type': chat.get('type'),
            }
        )

        if created:
            # this gets extra fields like description and profile pics
            blog.update_from_chat()

        message_type = get_message_type(message)
        if message_type is None:
            # other type of message like when a new user is added to a group
            return

        entry = Entry.objects.create(
            blog=blog,
            telegram_message_id=message['message_id'],
            message_json=json.dumps(message),
            type=message_type,
            message_time=datetime.fromtimestamp(message['date'], tz=timezone.utc)
        )

        entry.store_media_files()

    else:
        logger.info('Received update that is not a message')
        return


def get_telegram_file_download_link(file_id):
    data = request('getFile', data=dict(file_id=file_id))
    file_path = data['result']['file_path']
    token = get_bot_token()
    return f'https://api.telegram.org/file/bot{token}/{file_path}'


def get_telegram_file_content(file_id):
    url = get_telegram_file_download_link(file_id)
    r = session.get(url)
    r.raise_for_status()
    return BytesIO(r.content)
