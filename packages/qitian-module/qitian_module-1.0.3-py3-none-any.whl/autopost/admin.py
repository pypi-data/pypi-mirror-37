from django.contrib import admin
from autopost.models import AutoTask, Article, Category, Author
from django_celery_beat.models import PeriodicTask, PeriodicTasks, IntervalSchedule, CrontabSchedule
from system.utils.storage import HtmlStorage
from django.utils.html import format_html
from django.db.models.signals import post_save
import uuslug
import json


def add_celery(sender, instance, created, **kwargs):
    """
    创建定时任务
    :param sender:
    :param instance:
    :param created:
    :param kwargs:
    :return:
    """
    if created:
        periodic_task = PeriodicTask()
        periodic_task.crontab = instance.crontab
        periodic_task.task = 'autopost.tasks.crawl_news'
        periodic_task.args = '[%d]' % instance.id
        periodic_task.name = uuslug.slugify(instance.title + str(instance.site_id))
        periodic_task.save()
        instance.periodic_task = periodic_task
        instance.save()
    else:
        periodic_task = instance.periodic_task
        periodic_task.crontab = instance.crontab
        periodic_task.save()
    PeriodicTasks.changed(instance.periodic_task)


post_save.connect(add_celery, sender=AutoTask)


@admin.register(AutoTask)
class AutoTaskAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'crontab', 'url', 'site', 'category')
    list_display_links = ('id', 'title')
    list_filter = ('site', 'category')


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'category', 'get_site', 'publish_url', 'recommend_type', 'status', 'created')
    list_display_links = ('id', 'title')
    search_fields = ('title',)
    list_filter = ('site', 'category')
    list_editable = ('recommend_type',)

    def get_site(self, obj):
        return obj.category.site.name

    def publish_url(self, obj):
        purl = 'http://%s/news/%d.html' % (obj.category.site.domain, obj.id)
        return format_html('<a href="{url}" target="_blank">{url}</a>'.format(url=purl))

    get_site.short_description = '所属站点'
    publish_url.allow_tags = True
    publish_url.short_description = '发布URL'

    def save_model(self, request, obj, form, change):
        html_content, first_img, key_list, summery = HtmlStorage.save_content(obj.content, obj.save_img, obj.clear_link)
        obj.content = html_content
        if obj.thumbnail == '' and first_img:
            # 去掉前面/
            obj.thumbnail = first_img[1:]
        obj.keywords = ' '.join(key_list)
        if not obj.desc and summery:
            obj.desc = summery
        super(ArticleAdmin, self).save_model(request, obj, form, change)


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'created', 'updated']
    list_display_links = ('id', 'name')


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'parent', 'slug', 'site', 'status', 'created')
    list_display_links = ('id', 'name')
    list_filter = ('site',)
    list_editable = ('slug', 'status')
