from __future__ import absolute_import, unicode_literals
from celery import shared_task
from autopost.utils.crawler import QtCrawler


@shared_task
def crawl_news(task_id):
    qt_crawler = QtCrawler()
    qt_crawler.crawl_news(task_id)
    return True
