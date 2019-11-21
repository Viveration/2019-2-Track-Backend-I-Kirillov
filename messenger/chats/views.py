from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse, HttpResponseNotAllowed
from chats.models import Member, Chat
from django import forms


def index(request):
    if request.method != 'GET':
        return HttpResponseNotAllowed(['GET'])
    return render(request, 'index.html')


def chat_detail(request, pk):
    print(pk)
    if request.method == 'GET' or request.method == 'POST':
        return JsonResponse({'text': 'App'})
    else:
        return HttpResponseNotAllowed(['GET', 'POST'])


def chat_list(request, uid):
    if request.method == 'GET':
        member = Member.objects.filter(user=uid)
        list_of_chats = []
        for item in member:
            list_of_chats.push(*list(Chat.objects.first(id=item.chat)))
        return JsonResponse({
                'msg': list_of_chats
            })
    else:
        return HttpResponseNotAllowed(['GET'])


@csrf_exempt
def chat_create(request, uid):
    if request.method == 'POST':
        form = forms.ChatCreateForm(request.POST)
        if form.is_valid():
            chat = form.save()
            member = Member()
            member.user = int(uid)
            member.chat = chat.id
            member.new_messages = None
            member.last_read_message = None
            member.save()
            return JsonResponse({
                'msg': 'Чат создан'
                })
        else:
            return JsonResponse({"errors": "chatError"}, status=400)

    else:
        return HttpResponseNotAllowed(['POST'])


@csrf_exempt
def send_message(request, uid):
    if request.method == 'POST':
        form = forms.MessageSendFrom(request.POST)
        if form.id_valid():
            message = form.save()

            return JsonResponse({
                'msg': message
            })
        else:
            return JsonResponse({"errors": "messageError"}, status=400)
    else:
        return HttpResponseNotAllowed(['POST'])


def message_read(request):
    if request.method == 'GET':
        return JsonResponse({
            'msg': 'someText'
            })
    else:
        return HttpResponseNotAllowed(['GET'])
