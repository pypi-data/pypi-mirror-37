#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.core.mail import send_mail
from django.db import models
from django.utils.translation import ugettext_lazy as _

from .base import SerializableModel
from .db_constants import *

__all__ = ('Group', 'Language', 'Role', 'User', 'Discipline', 'Classroom', 'Article', 'Reaction', 'AttachmentType',
           'FileExtension', 'Attachment', 'Comment', 'Mention', 'Chat', 'ChatMember', 'Message', 'UserMessage')


class Role(SerializableModel):
    name = models.CharField(max_length=20, unique=True)

    __fields__ = ('name',)

    class Meta:
        verbose_name = _('Role')
        verbose_name_plural = _('Roles')
        db_table = '_Role'

    def __str__(self):
        return f'{self.name}'


class Group(SerializableModel):
    role = models.ForeignKey(Role, on_delete=models.SET_NULL, null=True, blank=True)
    code = models.CharField(max_length=10, unique=True)

    __fields__ = ('code', 'role_id')

    class Meta:
        verbose_name = _('Group')
        verbose_name_plural = _('Groups')
        db_table = '_Group'

    def __str__(self):
        return f'{self.code}'


class Language(SerializableModel):
    RU_RU = Language.RU_RU
    EN_US = Language.RU_RU
    LANG_CHOICES = (
        (RU_RU, 'Русский'),
        (EN_US, 'English')
    )
    code = models.CharField(choices=LANG_CHOICES, max_length=5, default=RU_RU, unique=True)

    __fields__ = ('code',)

    class Meta:
        verbose_name = _('Language')
        verbose_name_plural = _('Languages')
        db_table = '_Language'

    def __str__(self):
        return f'{self.code}'


class User(SerializableModel):
    first_name = models.CharField(max_length=64)
    last_name = models.CharField(max_length=64)
    group = models.ForeignKey(Group, on_delete=models.SET_NULL, null=True, blank=True)
    birthday = models.DateField(auto_now_add=True)
    about = models.TextField(max_length=1000, null=True, blank=True)
    profile_pic = models.ImageField(upload_to='media/users/profile_pics', null=True, blank=True)
    email = models.EmailField(max_length=100, unique=True)
    lang = models.ForeignKey(Language, on_delete=models.DO_NOTHING, null=True, blank=True)
    activated = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False, editable=False)

    __fields__ = ('first_name', 'last_name', 'group_id', 'about',
                  'profile_pic', 'email', 'lang_id', 'activated',)

    class Meta:
        verbose_name = _('User')
        verbose_name_plural = _('Users')
        db_table = '_User'

    def __str__(self):
        return f'{self.email} - {self.first_name} {self.last_name} [{self.group.code}]'

    def get_full_name(self):
        return '{} {}'.format(self.first_name, self.last_name)

    def get_short_name(self):
        return self.first_name

    def email_user(self, subject, message, from_email=None, **kwargs):
        send_mail(subject, message, from_email, [self.email], **kwargs)


class Discipline(SerializableModel):
    name = models.CharField(max_length=150, unique=True)

    __fields__ = ('name',)

    class Meta:
        verbose_name = _('Discipline')
        verbose_name_plural = _('Disciplines')
        db_table = '_Discipline'

    def __str__(self):
        return f'{self.name}'


class Classroom(SerializableModel):
    teacher = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    discipline = models.ForeignKey(Discipline, on_delete=models.DO_NOTHING)

    __fields__ = ('teacher_id', 'group_id', 'discipline_id',)

    class Meta:
        verbose_name = _('Classroom')
        verbose_name_plural = _('Classrooms')
        db_table = '_Classroom'
        unique_together = ('teacher', 'group', 'discipline')

    def __str__(self):
        return f'Discipline: {self.discipline.name}. Teacher: {self.teacher.get_full_name()}. Group: {self.group.code}'


class Article(SerializableModel):
    body = models.TextField(max_length=1000)
    timestamp = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    classroom = models.ForeignKey(Classroom, on_delete=models.DO_NOTHING, null=True, blank=True)
    private = models.BooleanField(default=False)

    __fields__ = ('body', 'user_id', 'classroom_id', 'private')

    class Meta:
        verbose_name = _('Article')
        verbose_name_plural = _('Articles')
        db_table = '_Article'

    def __str__(self):
        return f'{self.user.email} - {self.timestamp}'


class Reaction(SerializableModel):
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING, null=True, blank=True)

    __fields__ = ('article_id', 'user_id',)

    class Meta:
        verbose_name = _('Reaction')
        verbose_name_plural = _('Reactions')
        unique_together = ('article', 'user')
        db_table = '_Reaction'

    def __str__(self):
        return f'{self.user.email} liked {str(self.article)} article'


class AttachmentType(SerializableModel):
    tag = models.CharField(max_length=15, unique=True)

    __fields__ = ('tag',)

    class Meta:
        verbose_name = _('Attachment Type')
        verbose_name_plural = _('Attachment Types')
        db_table = '_AttachmentType'

    def __str__(self):
        return f'{self.tag}'


class FileExtension(SerializableModel):
    name = models.CharField(max_length=10, null=False, blank=False, unique=True)

    __fields__ = ('name',)

    class Meta:
        verbose_name = _('FileExtension')
        verbose_name_plural = _('FileExtensions')
        db_table = '_FileExtension'

    def __str__(self):
        return f'{self.name}'


class Attachment(SerializableModel):
    attachment_type = models.ForeignKey(AttachmentType, on_delete=models.DO_NOTHING)
    file = models.FileField(upload_to=f'media/attachments/{attachment_type}/')
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    original_name = models.CharField(max_length=100)
    file_extension = models.ForeignKey(FileExtension, on_delete=models.DO_NOTHING)

    __fields__ = ('attachment_type_id', 'article_id', 'original_name', 'file_extension_id',)

    class Meta:
        verbose_name = _('Attachment')
        verbose_name_plural = _('Attachments')
        db_table = '_Attachment'

    def __str__(self):
        return f'{self.file.name}'


class Comment(SerializableModel):
    body = models.TextField(max_length=150)
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)

    __fields__ = ('body', 'article_id', 'user_id')

    class Meta:
        verbose_name = _('Comment')
        verbose_name_plural = _('Comments')
        db_table = '_Comment'

    def __str__(self):
        return f"{self.user.email} commented under {self.article.user.email}'s article at {self.timestamp}"


class Mention(SerializableModel):
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE)
    had_seen = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)

    __fields__ = ('comment_id', 'had_seen', 'user_id')

    class Meta:
        verbose_name = _('Mention')
        verbose_name_plural = _('Mentions')
        unique_together = ('comment', 'user')
        db_table = '_Mention'

    def __str__(self):
        return f'{self.comment.user.email} mentioned {self.user.email} in his comment ({self.had_seen})'


class Chat(SerializableModel):
    class Meta:
        verbose_name = _('Chat')
        verbose_name_plural = _('Chats')
        db_table = '_Chat'

    def __str__(self):
        return f'{self.pk}'


class ChatMember(SerializableModel):
    chat = models.ForeignKey(Chat, related_name='chat_members', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)

    __fields__ = ('chat_id', 'user_id')

    class Meta:
        verbose_name = _('Chat Member')
        verbose_name_plural = _('Chat Members')
        unique_together = ('chat', 'user')
        db_table = '_ChatMember'

    def __str__(self):
        return f'Chat: {self.chat.pk}; User: {self.user.email}'


class Message(SerializableModel):
    body = models.TextField(max_length=150)
    chat = models.ForeignKey(Chat, related_name='messages', on_delete=models.CASCADE)
    sender = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    timestamp = models.DateTimeField(auto_now_add=True)

    __fields__ = ('body', 'chat_id', 'sender_id')

    class Meta:
        verbose_name = _('Message')
        verbose_name_plural = _('Messages')
        db_table = '_Message'

    def __str__(self):
        return f'Chat: {self.chat.pk}; Sender: {self.sender.pk}'


class UserMessage(SerializableModel):
    message = models.ForeignKey(Message, on_delete=models.DO_NOTHING)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    __fields__ = ('message_id', 'user_id')

    class Meta:
        verbose_name = _('User Message')
        verbose_name_plural = _('User Messages')
        unique_together = ('message', 'user')
        db_table = '_UserMessage'

    def __str__(self):
        return f'User: {self.user.pk}; Message: {self.message.pk}'
