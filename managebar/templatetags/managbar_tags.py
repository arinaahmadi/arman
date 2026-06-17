from django import template
from managebar.models import Barnameh

register = template.Library()

@register.simple_tag(name='getnumber')
def function():
    numberbarname = Barnameh.objects.all().count()
    return numberbarname

@register.inclusion_tag('managebar/listbar.html')
def list_bar():
    bars = Barnameh.objects.all()
    return {'bars':bars}

@register.inclusion_tag('managebar/detail_bar.html')
def detail_bar(shbar):
    bar = Barnameh.objects.get(shbarnameh=shbar)
    return {'bar':bar}