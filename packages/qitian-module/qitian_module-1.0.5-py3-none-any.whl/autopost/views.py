from django.views.generic import TemplateView, View
from django.http.response import HttpResponse, JsonResponse
from .utils.crawler import QtCrawler
from autopost.utils.crawler import QtCrawler


class IndexView(View):
    # template_name = ''

    def dispatch(self, request, *args, **kwargs):
        crawler = QtCrawler()
        my_url = 'https://www.huxiu.com/article/266497.html'
        title, html_content, first_img, key_words, summery = crawler.crawl_detail(my_url, 'h1', '.article-content-wrap',
                                                                                  '["div","div"]')
        return JsonResponse({'code': 200, 'msg': '处理完毕'})
