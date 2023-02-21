# Generated by Django 4.1.7 on 2023-02-21 07:41

import api.models
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Images',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image_orig', models.ImageField(null=True, upload_to=api.models.image_directory_path)),
                ('image_thumbnail_small', models.ImageField(null=True, upload_to=api.models.image_directory_path)),
                ('image_thumbnail_big', models.ImageField(null=True, upload_to=api.models.image_directory_path)),
                ('binary_image', models.BinaryField(null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'permissions': [('link_for_small_thumbnail', 'Сan get a link for a small thumbnail'), ('link_for_big_thumbnail', 'Сan get a link for a big thumbnail'), ('link_for_original_image', 'Сan get a link for an original image'), ('expiring_links_bin_image', 'Have ability to generate expiring links')],
            },
        ),
        migrations.CreateModel(
            name='BinaryImageTempLinks',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('life_time', models.IntegerField()),
                ('generated_uuid', models.CharField(max_length=36)),
                ('time_created', models.DateTimeField(auto_now_add=True)),
                ('image', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.images')),
            ],
        ),
    ]
