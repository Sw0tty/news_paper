from django.core.management.base import CommandError, BaseCommand
from news.models import Post


class Command(BaseCommand):
    help = "Просто есть"

    def handle(self, *args, **options):
        for post in Post.objects.all():
            self.stdout.write(self.style.SUCCESS("Yeap"))
