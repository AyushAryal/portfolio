import hashlib
from django import template

register = template.Library()


@register.filter()
def random_color(string):
    hash_value = int(hashlib.md5(string.encode()).hexdigest(), 16)
    hue = hash_value % 360
    saturation = 50
    lightness = 50
    hsl_color = f"hsl({hue}, {saturation}%, {lightness}%)"
    return hsl_color


@register.filter()
def random_number(string, final):
    hash_value = int(hashlib.md5(string.encode()).hexdigest(), 16)
    return hash_value % final
