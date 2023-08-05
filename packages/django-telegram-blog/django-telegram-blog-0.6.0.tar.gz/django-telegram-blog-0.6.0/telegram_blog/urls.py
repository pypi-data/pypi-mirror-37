from django.urls import path
from . import views
from telegram_blog.utils import get_webhook_hash

urlpatterns = [
    path('', views.Index.as_view(), name="index"),
    path('<int:pk>/', views.BlogDetailView.as_view(), name='blog_detail'),
    path('webhook/' + get_webhook_hash() + '/', views.WebhookView.as_view(), name='webhook'),
]

app_name = 'telegram_blog'
