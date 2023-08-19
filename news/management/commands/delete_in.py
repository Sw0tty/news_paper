from django.core.management.base import BaseCommand, CommandError
from news.models import Post, Category


class Command(BaseCommand):
    help = "Удаляет все записи в выбранной категории"

    def add_arguments(self, parser):
        parser.add_argument('category', type=str)

    def handle(self, *args, **options):
        self.stdout.write("Из какой категории удалить?")

        for category in Category.objects.all():
            self.stdout.write(f"{category.id} - {category}")

        category_answer = input()

        if category_answer in [name.category_name for name in Category.objects.all()]:
            self.stdout.write(f"Вы уверены, что хотите удалить все записи из категории '{category_answer}'?")
            self.stdout.write(f"Yes/no: ")
            answer = input()
        else:
            return self.stdout.write(self.style.ERROR(f"Категория '{category_answer}' не найдена"))

        if answer == 'Yes':

            # Post.objects.filter(category=category_answer).delete()

            self.stdout.write(self.style.SUCCESS(f"Все записи были удалены"))
        return self.stdout.write(self.style.ERROR("Неизвестная команда!"))
