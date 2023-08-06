from django import template
import random
import os
from django.conf import settings

register = template.Library()


@register.filter
def auto_thumbnail(img_src, alias):
    site, alias = site_image(alias)
    if str(img_src) == '':
        return settings.QINIU_RANDOM % random.randint(1, 15)
    return qiniu_max_thumbnail(img_src, alias)


def qiniu_max_thumbnail(image_src, alias):
    if str(image_src) == '':
        return ''
    if hasattr(settings, 'QINIU_THUMBNAIL') and 'max_limit' in settings.QINIU_THUMBNAIL:
        thumb_configure = settings.QINIU_THUMBNAIL['max_limit']
    else:
        return image_src
    if alias not in thumb_configure:
        return image_src
    try:
        return image_src.url + '?imageView2' + thumb_configure[alias]
    except Exception as e:
        return '/media/' + image_src


def site_image(alias):
    site = ''
    if alias.__contains__('__'):
        args = str(alias).split(',')
        site = args[0]
        alias = args[1]
    return site, alias
