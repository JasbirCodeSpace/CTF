from django.http.response import JsonResponse
from django.shortcuts import render
from accounts.models import Profile
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

@login_required
def solves_pie_chart(request):
    id = request.GET.get('id', None)
    if id is None:
        id = request.user.id
    user = User.objects.get(id=id)
    labels = ['correct', 'wrong']
    data = []
    correct = user.profile.submissions.filter(correct=True).count()
    wrong = solves = user.profile.submissions.filter(correct=False).count()
    data.append(correct)
    data.append(wrong)

    return JsonResponse(data={'labels': labels, 'data': data})

@login_required
def category_pie_chart(request):
    id = request.GET.get('id', None)
    if id is None:
        id = request.user.id
    user = User.objects.get(id=id)
    labels = []
    data = []
    solves = user.profile.submissions.filter(correct=True)
    solve_categories=[]

    for solve in solves:
        solve_categories.append(solve.challenge.category.name)

    category_count = {}
    for i in solve_categories:
        category_count[i] = category_count.get(i, 0) + 1

    for name,count in category_count.items():
        labels.append(name)
        data.append(count)

    return JsonResponse(data={'labels': labels, 'data': data})