from hashlib import md5
from urllib.parse import urljoin

from django.conf import settings
from django.urls import reverse

from requests import Session, RequestException
import logging


logger = logging.getLogger(__name__)

session = Session()


def get_bot_token():
    return getattr(settings, 'TELEGRAM_BLOG_BOT_TOKEN')  # type: str


def get_webhook_hash():
    token = get_bot_token()
    if token is None:
        return 'test'
    return md5(token.encode()).hexdigest()


def get_webhook_path():
    return reverse('webhook', urlconf='telegram_blog.urls')


def get_webhook_url():
    base_url = getattr(settings, 'TELEGRAM_BLOG_URL')
    if base_url is None:
        raise RuntimeError('TELEGRAM_BLOG_URL setting is empty')
    return urljoin(base_url, get_webhook_path())


def request(method, data=None):
    token = get_bot_token()
    if token is None:
        raise RuntimeError("TELEGRAM_BLOG_BOT_TOKEN is empty")
    url = f"https://api.telegram.org/bot{token}/{method}"
    r = session.post(url, data=data)
    try:
        r.raise_for_status()
    except RequestException:
        logger.exception(r.content)
    return r.json()
