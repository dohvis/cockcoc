import os
import json
from django.core.management.base import BaseCommand

from cockcoc.settings import BASE_DIR
from app.models import Cocktail

from django.core.files import File
class Command(BaseCommand):
    help = 'Load fixture data'

    @staticmethod
    def _get_image(url, name):
        from requests import get
        response = get(url)
        name = name.replace(" ", "_")
        filepath = os.path.join(BASE_DIR, 'media', 'cocktail_images', '%s.jpg' % name)
        with open(filepath, 'wb') as fp:
            fp.write(response.content)
        # 혼자쓸꺼니까 봐줘염
        return filepath.replace("/Users/nero/github/personal/cockcoc/", "")

    def add_arguments(self, parser):
        parser.add_argument('filepath', nargs='+', type=str)

    def handle(self, *args, **options):
        with open(options['filepath'][0], "r", encoding="utf8") as fp:
            cocktails = json.load(fp)
            for cocktail in cocktails:
                name = cocktail['name']
                description = cocktail['explanation']
                tags = cocktail['tag'].split(",")
                url = cocktail['img']
                image = self._get_image(url, name)
                print(image)
                cocktail_obj, created = Cocktail.objects.get_or_create(
                    name=name,
                    description=description,
                    image=File(open(image, 'rb'))
                )
                [cocktail_obj.tags.add(x) for x in tags]
                cocktail_obj.save()
