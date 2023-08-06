from django import template

register = template.Library()

# qsarg tags from here: https://github.com/simonw/simonwillisonblog/blob/3f5ca05248e409a946b53593f7d11b6f9551044f/blog/templatetags/blog_tags.py#L54-L68

@register.simple_tag(takes_context=True)
def add_qsarg(context, name, value):
    query_dict = context['request'].GET.copy()
    if value not in query_dict.getlist(name):
        query_dict.appendlist(name, value)
    return '?' + query_dict.urlencode()


@register.simple_tag(takes_context=True)
def remove_qsarg(context, name, value):
    query_dict = context['request'].GET.copy()
    query_dict.setlist(name, [
        v for v in query_dict.getlist(name) if v != value
    ])
    return '?' + query_dict.urlencode()
