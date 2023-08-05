from django import template
from bs4 import BeautifulSoup
from easy_thumbnails.files import get_thumbnailer

register = template.Library()


@register.filter
def html_first(value):
    soup = BeautifulSoup(value, 'lxml')
    first_img = soup.find('img')
    if not first_img:
        return None
    # return get_thumbnailer(first_img['src'])['content_related'].url
    return first_img['src']
