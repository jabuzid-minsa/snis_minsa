from django.template import Library
 
register = Library()
 
@register.filter(name='addclass')
def addclass(field, class_attr):
    return field.as_widget(attrs={'class': class_attr})

@register.simple_tag(takes_context=True)
def param_replace(context, **kwargs):
    d = context['request'].GET.copy()
    for k, v in kwargs.items():
        d[k] = v
    for k in [k for k, v in d.items() if not v]:
        del d[k]
    return d.urlencode()
