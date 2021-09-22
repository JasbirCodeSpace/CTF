from django import template

register = template.Library()

@register.filter(name='difficulty')
def difficulty(i):
    levels = ["Easy", "Medium", "Hard"]
    return levels[i-1]

@register.filter(name='correct_solves')
def correct_solves(submissions):
    submissions = submissions.filter(correct=True)
    return submissions

@register.filter(name='category_full_name')
def category_full_name(category):
    categories = {'WEB':"WEB EXPLOITATION", "FORENSIC":"FORENSIC", "REV":"REVERSE ENGINEERING", "CRYPTO": "CRYPTOGRAPHY", "MISC":"MISCELLANEOUS", "BLOCKCHAIN": "BLOCKCHAIN"}
    return categories[category]