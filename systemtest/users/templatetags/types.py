from django import template
register = template.Library()


@register.simple_tag
def to_list(*args):
    return args


@register.simple_tag
def define(val=None):
    return val

@register.filter(name='zip')
def zip_lists(a, b):
    return zip(a, b)
