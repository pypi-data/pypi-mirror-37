from app.models import Tag
from django.template import Library


register = Library()


@register.filter
def image_url(obj):
    temp = obj.imagecontentclass_set.all().order_by('pk')[0]
    return temp.image.url


@register.filter
def object_type(obj):
    return type(obj).__name__


@register.inclusion_tag('app/tagcloud.html')
def popular_tags():
    context = list(Tag.objects.all())[:10]
    return {'tags': context}



