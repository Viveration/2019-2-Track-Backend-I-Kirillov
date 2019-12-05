from django.shortcuts import render
from django.http import JsonResponse, HttpResponseNotAllowed
from userprofile.models import User
from django.forms import forms
from django.apps import apps
from django.contrib.auth.decorators import login_required


def contacts(request, uid):
    print('I dont know what to do, but I know ur ID: ', uid)
    if request.method == 'GET':
        return JsonResponse({'text': 'contacts ' + str(uid)})
    else:
        return HttpResponseNotAllowed(['GET'])


def profile(request, uid):
    print('I dont know what to do, but I know ur ID: ', uid)
    if request.method == 'GET' or request.method == 'POST':
        return JsonResponse({'text': 'profile ' + str(uid)})
    else:
        return HttpResponseNotAllowed(['GET', 'POST'])

@login_required
def user_search(request):
    if request.method == 'GET':
        users = User.objects.filter(username__contains=request.GET.get('name')).values('id', 'username', 'first_name')
        return JsonResponse({'users': list(users)})
    else:
        return HttpResponseNotAllowed(['GET'])
