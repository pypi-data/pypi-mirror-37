from django.db import models
from django.contrib.sites.models import Site
from smart_selects.db_fields import ChainedForeignKey
from ueditor import UEditorField
from mptt.models import MPTTModel, TreeForeignKey
from system.utils.storage import ImageStorage
from django_celery_beat.models import CrontabSchedule, PeriodicTask


class AutoTask(models.Model):
    title = models.CharField('任务名称', max_length=128)
    crontab = models.ForeignKey(CrontabSchedule, verbose_name='定时任务', on_delete=models.DO_NOTHING, blank=True,
                                null=True)
    url = models.CharField('抓取页面', max_length=255, blank=True, null=True)
    list_selector = models.CharField('列表规则', max_length=255, blank=True)
    page_selector = models.CharField('分页规则', max_length=255, blank=True)
    title_selector = models.CharField('标题规则', max_length=128, blank=True)
    content_selector = models.CharField('内容规则', max_length=128, blank=True)
    content_except = models.CharField('不包含内容', help_text='以json格式', max_length=255, blank=True, null=True)
    source = models.CharField('来源设定', max_length=128, blank=True)
    site = models.ForeignKey(Site, verbose_name='所属站点', on_delete=models.DO_NOTHING, blank=True, null=True)
    category = ChainedForeignKey('Category', verbose_name='所属分类', chained_field='site', chained_model_field='site',
                                 auto_choose=True)
    periodic_task = models.ForeignKey(PeriodicTask, verbose_name='定时任务', on_delete=models.DO_NOTHING, blank=True,
                                      null=True)
    created = models.DateTimeField('创建时间', auto_now_add=True)
    updated = models.DateTimeField('更新时间', auto_now=True)

    class Meta:
        db_table = 'auto_task'
        verbose_name = '抓取任务'
        verbose_name_plural = verbose_name
        ordering = ['-id']

    def __str__(self):
        return self.title


class CrawlLogs(models.Model):
    title = models.CharField('文章标题', max_length=255)
    url = models.CharField('文章URL', max_length=255)
    site_url = models.CharField('站点URL', max_length=128, blank=True, null=True)
    status = models.IntegerField('状态', choices=((1, '新增'), (2, '已抓取'), (3, '已修改')), default=1)
    site = models.ForeignKey(Site, verbose_name='所属站点', on_delete=models.DO_NOTHING, blank=True, null=True)
    created = models.DateTimeField('创建时间', auto_now_add=True)
    updated = models.DateTimeField('更新时间', auto_now=True)

    class Meta:
        db_table = 'crawl_logs'
        verbose_name = '抓取记录'
        verbose_name_plural = verbose_name + "管理"
        ordering = ['-id']

    def __str__(self):
        return self.title


class Category(MPTTModel):
    site = models.ForeignKey(Site, verbose_name='所属站点', on_delete=models.DO_NOTHING, default=1)
    parent = TreeForeignKey('self', verbose_name='上级菜单', null=True, blank=True, related_name='children',
                            on_delete=models.SET_NULL)
    name = models.CharField('名称', max_length=64)
    desc = models.TextField('描述', blank=True, null=True)
    status = models.IntegerField('状态', choices={(0, '隐藏'), (1, '显示'), (2, '主菜单')}, default=1)
    # 需要一个站点唯一
    slug = models.CharField('标识', max_length=128)
    url = models.CharField('地址', max_length=255, blank=True)
    created = models.DateTimeField('创建时间', auto_now_add=True)
    updated = models.DateTimeField('更新时间', auto_now=True)

    class MPTTMeta:
        order_insertion_by = ['id']
        get_ancestors = True

    class Meta:
        db_table = 'category'
        verbose_name = '分类'
        verbose_name_plural = verbose_name + '管理'
        ordering = ['id']

    def __str__(self):
        return self.name + '[%s]' % self.site.name


class Author(models.Model):
    name = models.CharField('名称', max_length=64)
    created = models.DateTimeField('创建时间', auto_now_add=True)
    updated = models.DateTimeField('更新时间', auto_now=True)

    class Meta:
        db_table = 'author'
        verbose_name = '作者'
        verbose_name_plural = verbose_name + '管理'

    def __str__(self):
        return self.name


class Article(models.Model):
    RC_TYPE = (
        (0, '不推荐'),
        (1, '幻灯'),
        (2, '焦点'),
        (3, '一级'),
        (4, '二级'),
        (5, '三级'),
    )

    site = models.ForeignKey(Site, verbose_name='所属站点', on_delete=models.DO_NOTHING, blank=True, null=True)
    category = ChainedForeignKey(Category, verbose_name='所属分类', chained_field='site', chained_model_field='site',
                                 auto_choose=True)
    title = models.CharField('标题', max_length=255)
    summery = models.TextField('摘要', blank=True, null=True)
    content = UEditorField('内容', blank=True, null=True)
    keywords = models.CharField('关键词', max_length=255, blank=True, null=True)
    author = models.ForeignKey('Author', verbose_name='作者', on_delete=models.DO_NOTHING, default=1)
    recommend_type = models.IntegerField('推荐类别', choices=RC_TYPE, default=0)
    thumbnail = models.ImageField('缩略图', upload_to='thumbnail/%Y/%m/%d', storage=ImageStorage(), blank=True)
    visits = models.IntegerField('访问数', default=1, blank=True)
    clear_link = models.BooleanField('清理链接', choices=((True, '是'), (False, '否')), default=True)
    save_img = models.BooleanField('保存图片', choices=((True, '是'), (False, '否')), default=True)
    status = models.BooleanField('是否显示', choices=((True, '显示'), (False, '隐藏')), default=True)
    created = models.DateTimeField('创建时间', auto_now_add=True)
    updated = models.DateTimeField('更新时间', auto_now=True)

    class Meta:
        db_table = 'article'
        verbose_name = '文章'
        verbose_name_plural = verbose_name + "管理"
        ordering = ['-id']

    def __str__(self):
        return self.title

    def increase_visit(self):
        self.visits += 1
        self.save()
        return self.visits
