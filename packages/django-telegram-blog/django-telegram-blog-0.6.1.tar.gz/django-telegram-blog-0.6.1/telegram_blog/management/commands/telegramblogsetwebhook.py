from django.core.management.base import BaseCommand
from telegram_blog.utils import request, get_webhook_url
from django.conf import settings


class Command(BaseCommand):
    help = 'Set Telegram webhook'

    def handle(self, *args, **options):

        max_connections = getattr(settings, 'TELEGRAM_BLOG_WEBHOOK_MAX_CONNECTIONS', 40)
        webhook_url = get_webhook_url()
        data = request('getWebhookInfo').get('result')
        self.stdout.write(f'existing webhook: {data}')
        if data['url'] != webhook_url or data['max_connections'] != max_connections:
            self.stdout.write(f'setting webhook with url {webhook_url} and max connections: {max_connections}')
            response = request('setWebhook', {
                'url': webhook_url,
                'max_connections': max_connections
            })
            self.stdout.write(f'setWebhook response: {response}')
        else:
            self.stdout.write('webhook config unchanged')


