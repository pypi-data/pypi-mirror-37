from django.core.management.base import BaseCommand
from telegram_blog.telegram import process_update
from telegram_blog.utils import get_bot_token, request
from django.conf import settings


class Command(BaseCommand):
    help = 'Connect to Telegram with long polling'

    def handle(self, *args, **options):

        offset = 0

        r = request('deleteWebhook')
        self.stdout.write(f"deleteWebhook: {r}")

        if settings.DEBUG:

            # self.stdout.write(session.get(f"https://api.telegram.org/bot{token}/getMe").text)
            pass

        while True:
            response = request('getUpdates', data=dict(timeout=60, offset=offset+1))
            if not response.get('ok'):
                self.stdout.write(response.get('description'))

            for update in response.get('result'):
                update_id = update.get('update_id')
                offset = max(update_id, offset)
                process_update(update)
