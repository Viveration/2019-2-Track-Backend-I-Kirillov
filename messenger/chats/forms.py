from django import forms
from userprofile.models import User
from chats.models import Chat, Message, Attachment, Member
import datetime


class ChatForm(forms.Form):
    topic = forms.CharField(max_length=64, initial='Title')
    is_group_chat = forms.BooleanField(initial=False, required=False)
    avatar = forms.FileField(required=False)
    members = forms.CharField()

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        super(ChatForm, self).__init__(*args, **kwargs)

    def clean_topic(self):
        topic = self.cleaned_data['topic']
        if (topic and len(topic) < 5):
            self.add_error('topic', 'Topic is too short!')
        return topic

    def clean(self):
        MAX_USERS_GROUP = 99
        MIN_USERS_GROUP = 2
        USER_NONGROUP = 1
        members = self.cleaned_data['members'].split('_')
        is_group_chat = self.cleaned_data['is_group_chat']
        members_list = []
        for user in members:
            try:
                user_for_list = User.objects.get(id=int(user))
            except User.DoesNotExist:
                self.add_error('members', 'Invalid members list')
                return None
            members_list.append(user_for_list)

        if self.user in members:
            self.add_error('members', "Can't create chat with yourself as a member!")

        if is_group_chat:
            if len(members) < MIN_USERS_GROUP:
                self.add_error('members', 'Too few members for group chat! (Should be more than 1)')
            elif len(members) > MAX_USERS_GROUP:
                self.add_error('members', 'Too much members! (Should be less than 100)')
        else:
            if len(members) != USER_NONGROUP:
                self.add_error('members', 'Only one member allowed for nongroup chat!')
            creator_chat = Member.objects.filter(user=members_list[0]).values_list('chat')
            target_chat = Member.objects.filter(user=self.user).values_list('chat')

            cross_chat = set(creator_chat) & set(target_chat)
            if len(cross_chat) > 0:
                self.add_error('members', 'Can not create chat due to it is already exist!')

    def save(self):
        data = self.cleaned_data
        topic = data['topic']
        is_group_chat = data['is_group_chat']
        members = data['members']
        chat = Chat.objects.create(topic=topic, is_group_chat=is_group_chat)

        Member.objects.create(user_id=self.user.id, chat=chat)
        for user in members:
            Member.objects.create(chat=chat, user_id=user.id)

        return chat


class SendMessageForm(forms.Form):
    content = forms.CharField(max_length=10000)
    chat_id = forms.IntegerField()

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        super(SendMessageForm, self).__init__(*args, **kwargs)

    def clean_chat_id(self):
        chat_id = self.cleaned_data['chat_id']
        try:
            Member.objects.get(chat_id=chat_id, user_id=self.user.id)
        except Member.DoesNotExist:
            self.add_error('chat_id', 'You are not member of this chat!')

        return chat_id

    def save(self):
        data = self.cleaned_data
        content = data['content']
        chat_id = data['chat_id']
        added_at = datetime.datetime.now()
        receivers = Member.objects.all().filter(chat_id=chat_id)
        for user in receivers:
            if user.user_id != self.user.id:
                user.new_messages += 1
                user.save()
            else:
                user.new_messages = 0
                user.save()

        message = Message.objects.create(user_id=self.user.id, chat_id=chat_id, added_at=added_at, content=content)
        chat = Chat.objects.get(id=chat_id)
        chat.last_message = message
        chat.save()
        member = Member.objects.get(user_id=self.user.id, chat_id=chat_id)
        member.last_read_message = message
        member.save()
        return message


class ReadMessageForm(forms.Form):
    chat_id = forms.IntegerField()

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        super(ReadMessageForm, self).__init__(*args, **kwargs)

    def clean_chat_id(self):
        chat_id = self.cleaned_data['chat_id']
        try:
            Member.objects.get(chat_id=chat_id, user_id=self.user.id)
        except Member.DoesNotExist:
            self.add_error('chat_id', 'You are not member of this chat!')
        return chat_id

    def save(self):
        data = self.cleaned_data
        chat_id = data['chat_id']
        chat = Chat.objects.get(id=chat_id)
        member = Member.objects.get(chat_id=chat_id, user_id=self.user.id)
        member.last_read_message_id = chat.last_message.id
        member.new_messages = 0
        member.save()
        message = Message.objects.get(id=chat.last_message.id)
        return message


class MessageList(forms.Form):
    chat_id = forms.IntegerField()

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        super(MessageList, self).__init__(*args, **kwargs)

    def clean_chat_id(self):
        chat_id = self.cleaned_data['chat_id']
        try:
            Member.objects.get(user_id=self.user.id, chat_id=chat_id)
        except Member.DoesNotExist:
            self.add_error('chat_id', 'Invalid chat_id!')
        return chat_id

    def save(self):
        data = self.cleaned_data
        chat_id = data['chat_id']
        message_list = list(Message.objects.all().filter(chat_id=chat_id).values('id', 'user_id', 'content'))
        return message_list


class AttachmentForm(forms.ModelForm):
    class Meta:
        model = Attachment
        fields = ['chat', 'user', 'message', 'mime_type', 'url']


class MemberForm(forms.ModelForm):
    class Meta:
        model = Member
        fields = ['user', 'chat', 'new_messages', 'last_read_message']