from setuptools import setup, find_packages

setup(
    name="django-telegram-blog",
    version="0.6.0",
    license="MIT",
    description="Blogging for Django via Telegram",
    author="Jaco du Plessis",
    author_email="jaco@jacoduplessis.co.za",
    packages=find_packages(),
    package_data={
        'telegram_blog': [
            'templates/telegram_blog/*.html',
        ]
    },
    install_requires=[
        "django",
        "requests",
        "python-magic",
    ],
)
