from django import template

register = template.Library()


@register.simple_tag(takes_context=True)
def set_qsarg(context, name, value):
    query_dict = context['request'].GET.copy()
    value = str(value)
    query_dict[name] = value
    return '?' + query_dict.urlencode()
