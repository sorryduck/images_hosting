from django.db import models

from django.contrib.auth.models import User
from django.db import models
from datetime import datetime


def image_directory_path(instance, filename):
    return 'images/{0}/{1}/{2}/{3}/{4}'.format(
        datetime.now().year,
        datetime.now().month,
        datetime.now().day,
        instance.user.username,
        filename
    )


class Images(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    image_orig = models.ImageField(upload_to=image_directory_path, null=True)
    image_thumbnail_small = models.ImageField(upload_to=image_directory_path, null=True)
    image_thumbnail_big = models.ImageField(upload_to=image_directory_path, null=True)
    binary_image = models.BinaryField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Image ID: {str(self.id)}'

    class Meta:
        permissions = [
            ("link_for_small_thumbnail", "Сan get a link for a small thumbnail"),
            ("link_for_big_thumbnail", "Сan get a link for a big thumbnail"),
            ("link_for_original_image", "Сan get a link for an original image"),
            ("expiring_links_bin_image", "Have ability to generate expiring links"),
        ]


class Binary_images_links(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ForeignKey(Images, on_delete=models.CASCADE)
    life_time = models.IntegerField()
    generated_uuid = models.CharField(max_length=36)
    time_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.time_created
