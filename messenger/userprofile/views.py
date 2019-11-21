from django.shortcuts import render
from django.http import JsonResponse, HttpResponseNotAllowed
from userprofile.models import User
from django.forms import forms


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
# Create your views here.


def user_search(request, name):
    if request.method == 'GET':
        user_list = list(User.objects.all())
        name_list = []
        for i in user_list:
            if i.nick == name:
                name_list.append(i.nick)
        return JsonResponse({'list': name_list})
        #user_list = list(user_list.get(nick__contains=str(name)))
        #if user_list is None:
         #   user_list = []
        #else:
        #    user_list = list(user_list)
        #return JsonResponse({'list': user_list})
    else:
        return HttpResponseNotAllowed(['GET'])
