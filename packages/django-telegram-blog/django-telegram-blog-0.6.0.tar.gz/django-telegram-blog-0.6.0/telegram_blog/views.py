from django.views.generic import View, ListView, DetailView, TemplateView
from django.http.response import HttpResponse
from .models import Blog, Entry
from .telegram import process_update
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.core.paginator import Paginator
import json

# Create your views here.


class Index(TemplateView):
    template_name = 'telegram_blog/index.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['blogs'] = Blog.objects.all()
        return ctx


@method_decorator(csrf_exempt, name='dispatch')
class WebhookView(View):
    def post(self, request):

        update = json.loads(request.body)
        process_update(update)
        return HttpResponse('OK')


class BlogDetailView(DetailView):
    model = Blog
    template_name = 'telegram_blog/blog_detail.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        entries = Entry.objects.filter(
            blog=self.object,
        ).order_by('-message_time')
        paginator = Paginator(entries, 20)
        page = self.request.GET.get('page')
        ctx['entries'] = paginator.get_page(page)
        return ctx
