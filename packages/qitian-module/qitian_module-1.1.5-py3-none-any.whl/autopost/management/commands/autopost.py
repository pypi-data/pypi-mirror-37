from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = '执行文章自动抓取'

    def add_arguments(self, parser):
        parser.add_argument('auto_id', nargs='+', type=int)

    def handle(self, *args, **options):
        print('获取远程文章抓取')

