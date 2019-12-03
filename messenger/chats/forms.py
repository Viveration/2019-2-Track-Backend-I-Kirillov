from django import forms
from userprofile.models import User
from chats.models import Chat, Message, Attachment, Member


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

    def clean_members(self):
        members = self.cleaned_data['members'].split('_')
        is_group_chat = self.cleaned_data['is_group_chat']
        members_list = []
        for user in members: 
            try:
                members_list.append(User.objects.get(id=int(user)))
            except User.DoesNotExist:
                self.add_error('members', 'Invalid members list')
                return None

        if self.user in members:
            self.add_error('members', "Can't create chat with yourself as a member!")

        if is_group_chat:
            if len(members) < 2:
                self.add_error('members', 'Too few members for group chat! (Should be more than 1)')
            elif len(members) >= 100:
                self.add_error('members', 'Too much members! (Should be less than 100)')
        else:
            if len(members) != 1:
                self.add_error('members', 'Only one member allowed for nongroup chat!')
            creator_chat = Member.objects.filter(user=members_list[0]).values_list('chat')
            target_chat = Member.objects.filter(user=self.user).values_list('chat')

            cross_chat = set(creator_chat) & set(target_chat)
            if len(cross_chat) > 0:
                self.add_error('members', 'Can not create chat due to it is already exist!')

        return members_list

    def save(self):
        data = self.cleaned_data
        topic = data['topic']
        is_group_chat = data['is_group_chat']
        members = data['members']
        chat = Chat.objects.create(topic=topic, is_group_chat=is_group_chat)

        Member.objects.create(user=self.user, chat=chat)
        for user in members:
            Member.objects.create(chat=chat, user=user)

        return chat


class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['chat', 'user', 'content']


class AttachmentForm(forms.ModelForm):
    class Meta:
        model = Attachment
        fields = ['chat', 'user', 'message', 'mime_type', 'url']


class MemberForm(forms.ModelForm):
    class Meta:
        model = Member
        fields = ['user', 'chat', 'new_messages', 'last_read_message']