from django.db import models

from location_field.models.plain import PlainLocationField
from taggit.managers import TaggableManager

MAX_SIZE = 5242880


class CockcocImageField(models.ImageField):
    def __init__(self, *args, **kwargs):
        self.content_types = kwargs.pop("content_types", ['image/png', 'image/jpeg'])
        self.max_upload_size = kwargs.pop("max_upload_size", MAX_SIZE)
        super(CockcocImageField, self).__init__(*args, **kwargs)

    def clean(self, *args, **kwargs):
        from django.forms import ValidationError
        from django.template.defaultfilters import filesizeformat
        data = super(CockcocImageField, self).clean(*args, **kwargs)

        file = data.file
        try:
            content_type = file.content_type
        except AttributeError:
            ext = file.name[-4:].lower()
            if ext == ".png":
                content_type = 'image/png'
            elif ext == ".jpg" or ext == ".jpeg":
                content_type = 'image/jpeg'
            else:
                raise ValidationError('지원하지 않는 파일 형식 입니다.')

        if content_type in self.content_types:
            if file.size > self.max_upload_size:
                raise ValidationError('{} 이하의 파일을 올려주세요. 업로드하신 파일 크기는 {} 입니다.'.format(
                    filesizeformat(self.max_upload_size),
                    filesizeformat(file.size)
                ))
        else:
            raise ValidationError('지원하지 않는 파일 형식 입니다.')

        return data


class Cocktail(models.Model):
    name = models.CharField(max_length=28, unique=True)
    description = models.CharField(max_length=2000)
    tags = TaggableManager()
    image = CockcocImageField(
        content_types=['image/png', 'image/jpeg'],
        max_upload_size=MAX_SIZE,
        null=True,
        upload_to='cocktail_images',
    )

    def __str__(self):
        return "<Cocktail: {}>".format(self.name)


class Bar(models.Model):
    name = models.CharField(max_length=64)
    address = models.CharField(max_length=128, blank=True)
    description = models.TextField(blank=True)
    phone = models.CharField(max_length=32, blank=True)
    lng = models.FloatField()
    lat = models.FloatField()
    location = PlainLocationField(zoom=16, blank=True)
    image = CockcocImageField(
        content_types=['image/png', 'image/jpeg'],
        max_upload_size=MAX_SIZE,
        null=True,
        upload_to='bar_images',
    )
    cocktails = models.ManyToManyField(Cocktail, related_name='bars')

    def __str__(self):
        return "<Bar: {}>".format(self.name)

    def save(self, *args, **kwargs):
        if len(self.location) < 1:  # if new objects
            self.location = "{},{}".format(str(self.lat), str(self.lng))
        locations = self.location.split(",")
        if locations != [float(self.lat), float(self.lng)]:
            self.lat = locations[0]
            self.lng = locations[1]
        super(Bar, self).save(*args, **kwargs)
