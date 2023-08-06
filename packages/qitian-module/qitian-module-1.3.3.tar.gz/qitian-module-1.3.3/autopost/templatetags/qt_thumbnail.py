from django import template
import random
import os
from django.conf import settings
from urllib import request
from urllib.error import HTTPError

register = template.Library()


@register.filter
def auto_thumbnail(img_src, alias):
    site, alias = site_image(alias)
    if str(img_src) == '':
        return settings.QINIU_RANDOM % random.randint(1, 15)
    return qiniu_max_thumbnail(img_src, alias)


def qiniu_max_thumbnail(image_src, alias):
    if hasattr(settings, 'QINIU_THUMBNAIL') and 'max_limit' in settings.QINIU_THUMBNAIL:
        thumb_configure = settings.QINIU_THUMBNAIL['max_limit']
    else:
        return get_url_code(image_src)
    if alias not in thumb_configure:
        return get_url_code(image_src)
    zoom_name = '?imageView2' + thumb_configure[alias]
    try:
        return get_url_code(image_src.url, zoom_name)
    except Exception as e:
        return get_url_code(settings.MEDIA_URL + str(image_src), zoom_name)


def get_url_code(img_url, alias=''):
    try:
        request.urlopen(img_url, timeout=1)
        return img_url + alias
    except Exception:
        return settings.QINIU_RANDOM % random.randint(1, 15) + alias


def site_image(alias):
    site = ''
    if alias.__contains__('__'):
        args = str(alias).split(',')
        site = args[0]
        alias = args[1]
    return site, alias
