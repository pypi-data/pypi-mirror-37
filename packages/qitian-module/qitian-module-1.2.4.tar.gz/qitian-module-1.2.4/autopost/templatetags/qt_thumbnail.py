from django import template
from easy_thumbnails.files import get_thumbnailer
import random
from django.conf import settings

register = template.Library()


@register.filter
def auto_thumbnail(img_src, alias):
    site, alias = site_image(alias)
    if str(img_src) == '':
        img_src = settings.QINIU_RANDOM % random.randint(1, 15)
    if str(img_src).__contains__(settings.QINIU_URL):
        return qiniu_max_thumbnail(img_src, alias)
    site, alias = site_image(alias)
    try:
        thumb = get_thumbnailer(img_src)[alias]
    except Exception:
        return ''
    return thumb.url


def qiniu_max_thumbnail(image_src, alias):
    if str(image_src) == '':
        return ''
    site, alias = site_image(alias)
    if hasattr(settings, 'QINIU_THUMBNAIL') and 'max_limit' in settings.QINIU_THUMBNAIL:
        thumb_configure = settings.QINIU_THUMBNAIL['max_limit']
    else:
        return image_src
    return str(image_src) + '?imageView2' + thumb_configure[alias]


def site_image(alias):
    site = ''
    if alias.__contains__('__'):
        args = str(alias).split(',')
        site = args[0]
        alias = args[1]
    return site, alias
