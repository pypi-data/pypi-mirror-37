from django.views.generic import TemplateView, View
from django.http.response import HttpResponse, JsonResponse
from .utils.crawler import QtCrawler
from autopost.utils.crawler import QtCrawler
from urllib import parse


class IndexView(View):
    # template_name = ''

    def dispatch(self, request, *args, **kwargs):
        crawler = QtCrawler()
        my_url = 'https://www.huxiu.com/article/266497.html'
        title, html_content, first_img, key_words, summery = crawler.crawl_detail(my_url, 'h1', '.article-content-wrap',
                                                                                  '["div","div"]')
        return JsonResponse({'code': 200, 'msg': '处理完毕'})


class PreviewList(View):
    def dispatch(self, request, *args, **kwargs):
        ret_data = {'code': 400, 'data': []}
        crawler = QtCrawler()
        url = parse.unquote(request.GET.get('page_url'))
        patterns = parse.unquote(request.GET.get('pattern'))
        if url and patterns:
            articles = crawler.crawl_list(url, patterns, True)
            ret_data['code'] = 200
            ret_data['data'] = articles
        return JsonResponse(ret_data)


class PreviewDetail(TemplateView):
    def dispatch(self, request, *args, **kwargs):
        ret_data = {'code': 400, 'data': []}
        crawler = QtCrawler()
        detail_url = parse.unquote(request.GET.get('detail_url'))
        title_pattern = parse.unquote(request.GET.get('title_pattern'))
        content_pattern = parse.unquote(request.GET.get('content_pattern'))
        exclude_pattern = parse.unquote(request.GET.get('exclude_pattern'))
        lazy_photo = parse.unquote(request.GET.get('lazy_photo'))
        if detail_url and title_pattern and content_pattern:
            title, main_content = crawler.crawl_detail(detail_url, title_pattern, content_pattern, exclude_pattern,
                                                       lazy_photo, fetch_img=True, preview=True)
            ret_data['code'] = 200
            ret_data['data'] = {'title': title, 'content': str(main_content)}
        return JsonResponse(ret_data)
