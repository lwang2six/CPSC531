import os
import Image

from django.template import Library
from django.conf import settings

register = Library()

def URL_PREFIX():
    return settings.URL_PREFIX
register.simple_tag(URL_PREFIX)

def STATIC_PREFIX():
    return settings.STATIC_PREFIX
register.simple_tag(STATIC_PREFIX)

@register.filter(name='get_pages')
def get_pages(value, arg=''):
    s = x = ''
    if arg:
        x = 'min_support=%s&' % arg
    if int(value.paginator.num_pages)-int(value.number) > 3  and int(value.number) > 4 or int(value.number) -1 > 3 and int(value.number) < 4 or int(value.number) == 4:
        s = '1 ... <a href="?%spage=%s">%s</a> <strong>%s</strong> <a href="?page=%s">%s</a> ...%s' % (x, value.previous_page_number(), value.previous_page_number(), value.number, value.next_page_number(), value.next_page_number(), value.paginator.num_pages)  
     
    else:
        if int(value.number)-1 < 3:
            s = ''
            for i in range(1,4):
                if int(value.number) == i:
                    s += '<strong>%s</strong> ' % i
                else:
                    s += '<a href="?%spage=%s">%s</a> ' % (x, i, i)
            s += ' ... <a href="?%spage=%s">%s</a>' % (x, int(value.paginator.num_pages), int(value.paginator.num_pages))
        else:
            s = '<a href="?%spage=1">1</a> ... ' % x
            for i in reversed(range(3)):
                num = int(value.paginator.num_pages)-int(i)
                if int(value.number) == num:
                    s += '<strong>%s</strong> ' % num
                else:
                    s += '<a href="?%spage=%s">%s</a> ' % (x, num, num)
    return s
register.filter(get_pages)


