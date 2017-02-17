import os
import json
from django.core.management.base import BaseCommand
from app.models import Bar

from django.core.files import File


class Command(BaseCommand):
    help = 'Load fixture data'

    def add_arguments(self, parser):
        parser.add_argument('filepath', nargs='+', type=str)

    def handle(self, *args, **options):
        with open(options['filepath'][0], "r", encoding="utf8") as fp:
            bars = json.load(fp)
            for bar in bars:
                name = bar['name']
                address = bar['address']
                phone = bar['telDisplay']
                x = bar['x']
                y = bar['y']
                fn = 'static/images/bar_images/%s.jpg' % name.replace(" ", "_")
                try:
                    print(name)
                    bar_objects = Bar.objects.create(
                        name=name,
                        address=address,
                        phone=phone,
                        lat=x,
                        lng=y,
                        image=File(open(fn, 'rb'))
                    )
                except FileNotFoundError:
                    pass
