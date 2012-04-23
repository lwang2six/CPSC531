from django.template import Library

register = Library()

@register.filter(name='process_fields')
def process_fields(arg):
    s = ''
    try:
        for i in arg.split(','):
            key, value = i.split(':')
            s += '%s = %s, ' % (key.title(), value)

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



