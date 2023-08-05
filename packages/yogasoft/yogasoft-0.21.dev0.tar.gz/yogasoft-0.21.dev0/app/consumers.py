import json
from .models import Comment, CommentSecondLevel
from channels import Group
from django.db.models.signals import post_save
from django.dispatch.dispatcher import receiver


def ws_connect(message):
    blog_id = message['path'].strip('/')
    message.reply_channel.send({"accept": True })
    # Add them to the chat group
    Group("%s" % blog_id).add(message.reply_channel)

def ws_disconnect(message):
    blog_id = message['path'].strip('/')
    Group("%s" % blog_id).discard(message.reply_channel)

def ws_message(message):
    pass

@receiver(post_save)
def send_update(sender, instance, **kwargs):
    list_of_models = ('Comment', 'CommentSecondLevel')
    if isinstance(instance, Comment):
        blog = instance.blog
        Group(str(blog.id)).send({
            'text': json.dumps({
                'comment_id': str(instance.id),
                'author_name': str(instance.author_name),
                'time': instance.time.strftime("%b %d, %Y, %H:%M %p"),
                'message': str(instance.message),
                'second_comment': 'False',
            }),
        })
    elif isinstance(instance, CommentSecondLevel):
        blog = instance.father_comment.blog
        Group(str(blog.id)).send({
            'text': json.dumps({
                'comment_id': str(instance.id),
                'father_comment_id': str(instance.father_comment.id),
                'author_name': str(instance.author_name),
                'time': instance.time.strftime("%b %d, %Y, %H:%M %p"),
                'message': str(instance.message),
                'second_comment': 'True',
            }),
        })








