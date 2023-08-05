from django.contrib import admin
from autopost.models import AutoTask, Article, Category, Author, RemoteImages
from django_celery_beat.models import PeriodicTask, PeriodicTasks, IntervalSchedule, CrontabSchedule
from autopost.utils.html import HtmlStorage
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
    # fields = ('preview_title_btn','title')
    fieldsets = (
        ('基础设置', {'fields': ['title', 'url', 'crontab']}),
        ('文章列表', {'fields': ['list_selector', 'page_selector', 'preview_title_btn']}),
        ('文章内容', {'fields': ['title_selector', 'content_selector', 'content_except', 'preview_detail_btn']}),
        ('发布设置', {'fields': ['site', 'category', 'source', 'author']}),
    )
    readonly_fields = ('preview_title_btn', 'preview_detail_btn')

    class Media:
        js = ('qt_admin/js/autopost.js',)
        css = {'all': ('qt_admin/css/bootstrap.css',)}


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
        if obj.thumbnail == '' and first_img and first_img.startswith('/'):
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


@admin.register(RemoteImages)
class RemoteImagesAdmin(admin.ModelAdmin):
    list_display = ('id', 'file_name', 'origin_src', 'local_src', 'remote_src', 'created')
    list_display_links = ('id', 'file_name')
    list_filter = ('file_name', 'remote_src', 'origin_src')
