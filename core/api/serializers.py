import imghdr
import os
from rest_framework import serializers
from .models import *


def validate_image(value):
    valid_extensions = ['.png', '.jpg', '.jpeg']
    file_extension = os.path.splitext(value.name)[1].lower()

    if file_extension not in valid_extensions:
        raise serializers.ValidationError("Unsupported file type. Only PNG and JPEG files are allowed.")

    file_type = imghdr.what(value)
    if file_type not in ['png', 'jpeg']:
        raise serializers.ValidationError("Invalid image format. Only PNG and JPEG images are allowed.")

    return value


def validate_life_time(value):
    if value < 300 or value > 300_000:
        raise serializers.ValidationError(
            "Value of links lifetime should be less than 300001 and higher than 299 seconds")

    return value


class ImageCreateSerializer(serializers.Serializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    image_orig = serializers.ImageField(validators=[validate_image])

    def create(self, validated_data):
        return Images.objects.create(**validated_data)


class ImageListSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    image_orig = serializers.ImageField()
    image_thumbnail_small = serializers.ImageField()
    image_thumbnail_big = serializers.ImageField()


class TempLinkGeneratorSerializer(serializers.Serializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    image = serializers.PrimaryKeyRelatedField(queryset=Images.objects.all(), )
    life_time = serializers.IntegerField(validators=[validate_life_time])

    def create(self, validated_data):
        return Binary_images_links.objects.create(**validated_data)


class TempLinkListSerializer(serializers.Serializer):
    image = serializers.PrimaryKeyRelatedField(queryset=Images.objects.all())
    life_time = serializers.IntegerField()
    generated_uuid = serializers.CharField()
    time_created = serializers.DateTimeField()
