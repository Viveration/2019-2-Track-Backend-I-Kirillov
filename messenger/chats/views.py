from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse, HttpResponseNotAllowed
from chats.models import Member, Chat, Message
from userprofile.models import User
import datetime

from chats.forms import ChatForm, MemberForm, MessageForm, AttachmentForm
from django import forms
from django.apps import apps


def index(request):
    if request.method != 'GET':
        return HttpResponseNotAllowed(['GET'])
    return render(request, 'index.html')


def chat_detail(request, chat_id):
    if request.method == 'GET' or request.method == 'POST':
        Chat = apps.get_model('chats', 'Chat')
        chat = Chat.objects.filter(id=chat_id).values('id', 'is_group_chat', 'topic', 'last_message').first()
        return JsonResponse({'foundChat': list(chat)})
    else:
        return HttpResponseNotAllowed(['GET', 'POST'])


def chat_list(request):
    if request.method == 'GET':
        chats = Chat.objects.all().values('id', 'is_group_chat', 'topic', 'last_message')
        return JsonResponse({
                'list': list(chats)
            })
    else:
        return HttpResponseNotAllowed(['GET'])


@csrf_exempt
def chat_create(request):
    if request.method == 'GET':
        form = ChatForm(request.GET, user=request.user)
        if form.is_valid():
            chat = form.save()
        else: 
            return JsonResponse({'errors': form.errors})
        return JsonResponse({'chat': chat.id,
                             'topic': chat.topic
                             })
    else:
        return HttpResponseNotAllowed(['GET'])


@csrf_exempt
def read_message(request):
    if request.method == 'POST':
        Member = apps.get_model('chats', 'Member')
        Message = apps.get_model('chats', 'Message')

        message = Message.objects.filter(id=int(request.POST.get('message_id', 12))).first()

        if message:
            member = Member.objects.filter(user_id=int(request.POST.get('user_id', 3)), chat=message.chat_id).first()

            if member:

                if member.last_read_message == None or member.last_read_message_id < int(request.POST['message_id']):
                    member.last_read_message_id = int(request.POST['message_id'])
                    member.save()

                return JsonResponse({'message_id': member.last_read_message_id})

            return JsonResponse({'member': 'Member not found'}, status=400)

        return JsonResponse({'message': 'Message not found'}, status=400)
    else:
        return HttpResponseNotAllowed(['POST'])


def chat_messages_list(request):
    if request.method == 'GET':
        Message = apps.get_model('chats', 'Message')

        messages = Message.objects.filter(chat_id=int(request.GET.get('chat_id', False))).values('id', 'chat_id', 'user_id', 'content', 'added_at')
        return JsonResponse({'messages': list(messages)})
    else:
        return HttpResponseNotAllowed(['GET'])

@csrf_exempt
def send_message(request):
    if request.method == 'POST':
        Member = apps.get_model('chats', 'Member')
        Chat = apps.get_model('chats', 'Chat')

        form = MessageForm(request.POST)

        if form.is_valid():
            message = form.save()

            msg = {'id': message.id, 'chat_id': message.chat.id, 'user_id': message.user.id, 'content': message.content, 'added_at': message.added_at}

            chat = Chat.objects.filter(id=message.chat.id).first()

            if chat:
                chat.last_message = message.content
                chat.save()

            members = list(Member.objects.filter(chat=message.chat.id).exclude(user_id=message.user.id))
            for member in members:
                member.save()

            return JsonResponse({'message': msg})

        return JsonResponse({'errors': form.errors}, status=400)
    else:
        return HttpResponseNotAllowed(['POST'])

#        union_of_chats = list(member1_chat_set & member2_chat_set)
#        if union_of_chats:
#            for item in union_of_chats:
#                chat = Chat.objects.filter(id=item[0]).first()
#
#                if not chat.is_group_chat:
#                    chat_json = {'id': chat.id, 'is_group_chat': chat.is_group_chat, 'topic': chat.topic, 'last_message': chat.last_message}
#                    return JsonResponse({'chat': chat_json})
#member1_chat_set = set(Member.objects.filter(user_id=uid).values_list('chat_id'))
#member2_chat_set = set(Member.objects.filter(user_id=target_user_id).values_list('chat_id'))


# deep dark databases fill

def database_fill(request):
    User.objects.all().filter(username='viveration').delete()
    User.objects.all().filter(username='refrigeratorr').delete()
    User.objects.all().filter(username='v1ad0S').delete()
    Chat.objects.all().filter(topic='TopHata').delete()
    Chat.objects.all().filter(topic='Ashen One').delete()
    Chat.objects.all().filter(topic='I dont want to delete this view').delete()
    user1 = User.objects.create(password='123', is_superuser=False, username='viveration', first_name='Ivan', last_name='Kirillov', email='viveration@mail.ru', is_staff=True, is_active=True, nick='viveration', date_joined=datetime.datetime.now())
    user2 = User.objects.create(password='123', is_superuser=False, username='refrigeratorr', first_name='Egor', last_name='Konukhov', email='', is_staff=True, is_active=True, nick='refrigeratorr', date_joined=datetime.datetime.now())
    user3 = User.objects.create(password='123', is_superuser=False, username='v1ad0S', first_name='Vladislav', last_name='Illarionov', email='', is_staff=True, is_active=True, nick='v1ad0S', date_joined=datetime.datetime.now())
    chat1 = Chat.objects.create(topic='TopHata', is_group_chat=True)
    chat2 = Chat.objects.create(topic='Ashen One', is_group_chat=True)
    chat3 = Chat.objects.create(topic='I dont want to delete this view', is_group_chat=True)
    Member.objects.create(chat_id=chat1.id, user_id=user1.id)
    Member.objects.create(chat_id=chat1.id, user_id=user2.id)
    Member.objects.create(chat_id=chat2.id, user_id=user2.id)
    Member.objects.create(chat_id=chat2.id, user_id=user3.id)
    Member.objects.create(chat_id=chat3.id, user_id=user1.id)
    Member.objects.create(chat_id=chat3.id, user_id=user2.id)
    Member.objects.create(chat_id=chat3.id, user_id=user3.id)
    Message.objects.create(chat_id=chat1.id, user_id=user1.id, content='1: chat1 user1')
    Message.objects.create(chat_id=chat1.id, user_id=user2.id, content='1: chat1 user2')
    Message.objects.create(chat_id=chat1.id, user_id=user1.id, content='2: chat1 user1')
    Message.objects.create(chat_id=chat2.id, user_id=user2.id, content='1: chat2 user2')
    Message.objects.create(chat_id=chat2.id, user_id=user3.id, content='1: chat2 user3')
    Message.objects.create(chat_id=chat2.id, user_id=user2.id, content='2: chat2 user2')
    Message.objects.create(chat_id=chat2.id, user_id=user3.id, content='2: chat2 user3')
    Message.objects.create(chat_id=chat3.id, user_id=user1.id, content='1: chat3 user1')
    Message.objects.create(chat_id=chat3.id, user_id=user1.id, content='2: chat3 user1')
    Message.objects.create(chat_id=chat3.id, user_id=user2.id, content='1: chat1 user2')
    Message.objects.create(chat_id=chat3.id, user_id=user3.id, content='1: chat1 user3')
    return JsonResponse({'fill': 'noerrors'}, status=400)
