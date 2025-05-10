from django import template
from urllib.parse import urlencode

register = template.Library()

@register.simple_tag
def querystring(params, key, value):
    """
    Toma QueryDict 'params', reemplaza/añade el par (key, value) y devuelve la nueva query string.
    Uso: {% querystring request.GET 'page' 3 %}
    """
    q = params.copy()
    q[key] = value
    return q.urlencode()
