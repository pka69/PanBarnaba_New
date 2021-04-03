import random

from django import template
from django.contrib.humanize.templatetags.humanize import intcomma

register = template.Library()

@register.simple_tag
def define(val=None):
  return val

@register.simple_tag
def sum(a, b):
    return a+b

@register.simple_tag
def sub(a, b):
    return a-b

@register.filter
def addstr(a, b):
  return str(a) + str(b)
  
@register.simple_tag
def range_gen(number):
  return range(number)

@register.filter
def no_records(data):
  return '{:,}'.format(data.count())

@register.filter
def web_adress(link):
  return True if link.startswith('http') else False

@register.filter
def shuffle(arg):
    return sorted(arg, key=lambda x: random.random())
