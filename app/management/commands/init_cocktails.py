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
        filepath = os.path.join('static/images', 'cocktail_images', '%s.jpg' % name)
        with open(filepath, 'wb') as fp:
            fp.write(response.content)
        return filepath

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
                fn = 'static/images/cocktail_images/%s.jpg' % name.replace(" ", "_")

                try:
                    cocktail_obj = Cocktail.objects.get(name=name)
                    fp = File(open(fn, 'rb'))
                    cocktail_obj.image = fp
                    cocktail_obj.save()
                except Cocktail.DoesNotExist:
                    fn = self._get_image(url, name)
                    print(fn)
                    fp = open(fn, 'rb')
                    cocktail_obj = Cocktail.objects.create(
                        name=name,
                        description=description,
                    )
                    cocktail_obj.image = File(fp)
                    cocktail_obj.save()

                [cocktail_obj.tags.add(x) for x in tags]
                cocktail_obj.save()
