from django import template

register = template.Library()

@register.filter(name='difficulty')
def difficulty(i):
    levels = ["Easy", "Medium", "Hard"]
    return levels[i]

@register.filter(name='correct_solves')
def correct_solves(submissions):
    submissions = submissions.filter(correct=True)
    return submissions