from django.template import Library
from record.models import Subset
register = Library()

@register.filter(name='process_fields')
def process_fields(arg, line_break=None):
    s = ''
    try:
        count = 0
        for i in arg.split(','):
            if i != '':
                key, value = i.split(':')
                if key.title() == 'Income' and value != 'ANY':
                    s += 'Income %s, ' % ('> 50K' if value == '1' else '=< 50K')
                else:
                    s += '%s = %s, ' % (key.title(), value)
            if line_break:
                if count == line_break:
                    count=0
                    s += '<br/>'
                count = count + 1
                
        return s[:-2].replace('_',' ')
    except:
        return arg
register.filter(process_fields)

@register.filter(name='paramfilter')
def paramfilter(value, arg):
    return value.order_by(arg)
register.filter(paramfilter)

@register.filter(name='rstrip')
def rstrip(value):
    return str(value).rstrip('0')
register.filter(rstrip)

@register.filter(name='dire')
def dire(value):
    return value
register.filter(dire)

