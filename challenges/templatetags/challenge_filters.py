from django import template

register = template.Library()

@register.filter(name='difficulty')
def difficulty(i):
    levels = ["Easy", "Medium", "Hard"]
    return levels[i]
