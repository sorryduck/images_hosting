import uuid
from io import BytesIO
from django.core.files.base import ContentFile
from django.http import HttpResponse
from rest_framework import permissions, viewsets, status
from PIL import Image
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from django.utils import timezone
from .serializers import *
from .models import *


class ImageAPIViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Images.objects.filter(user_id=self.request.user.id).order_by('-id')

    def get_serializer_class(self):
        if self.action == 'list':
            return ImageListSerializer
        elif self.action == 'create':
            return ImageCreateSerializer

    @staticmethod
    def make_thumbnails(size, serializer):

        thumbnail_obj = serializer.validated_data.get('image_orig')
        thumbnail_pillow = Image.open(thumbnail_obj)
        thumbnail_pillow.thumbnail(size)
        buffer_for_thumbnail = BytesIO()
        thumbnail_pillow.save(buffer_for_thumbnail, format='PNG')

        return ContentFile(buffer_for_thumbnail.getvalue(), name=f'{size[0]}px_thumbnail_{thumbnail_obj.name}')

    @staticmethod
    def make_binary_image(serializer):

        binary_image = Image.open(serializer.validated_data.get('image_orig'))
        buffer_binary_image = BytesIO()
        binary_image.save(buffer_binary_image, format='PNG')

        return buffer_binary_image.getvalue()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):

        if self.request.user.has_perm('api.link_for_small_thumbnail'):
            image_thumbnail_small = self.make_thumbnails((200, 200), serializer)
        else:
            image_thumbnail_small = None

        if self.request.user.has_perm('api.link_for_big_thumbnail'):
            image_thumbnail_big = self.make_thumbnails((400, 400), serializer)
        else:
            image_thumbnail_big = None

        if self.request.user.has_perm('api.expiring_links_bin_image'):
            binary_image = self.make_binary_image(serializer)
        else:
            binary_image = None

        if self.request.user.has_perm('api.link_for_original_image'):
            image_orig = serializer.validated_data.get('image_orig')
        else:
            image_orig = None

        serializer.save(
            image_thumbnail_small=image_thumbnail_small,
            image_thumbnail_big=image_thumbnail_big,
            binary_image=binary_image,
            image_orig=image_orig,
        )


class TempLinkAPI(viewsets.ModelViewSet):
    permissions = [permissions.IsAuthenticated]
    uuid_link = uuid.uuid4()

    def get_queryset(self):
        return Binary_images_links.objects.filter(user_id=self.request.user.id)

    def get_serializer_class(self):
        if self.action == 'list':
            return TempLinkListSerializer
        elif self.action == 'create':
            return TempLinkGeneratorSerializer

    def list(self, request, *args, **kwargs):
        print(request.user.id)
        if self.request.user.has_perm('api.expiring_links_bin_image'):
            queryset = self.filter_queryset(self.get_queryset())

            page = self.paginate_queryset(queryset)
            if page is not None:
                serializer = self.get_serializer(page, many=True)
                return self.get_paginated_response(serializer.data)

            serializer = self.get_serializer(queryset, many=True)
            return Response(serializer.data)
        else:
            return Response(status=status.HTTP_403_FORBIDDEN)

    def create(self, request, *args, **kwargs):

        if self.request.user.has_perm('api.expiring_links_bin_image') \
                and Images.objects.get(id=request.data['image']).user_id == request.user.id:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            link = f'/api/{self.uuid_link}'
            return Response({'link': link}, status=status.HTTP_201_CREATED, headers=headers)
        else:
            return Response(status=status.HTTP_403_FORBIDDEN)

    def perform_create(self, serializer):
        serializer.save(
            generated_uuid=self.uuid_link,
        )

    def retrieve(self, request, *args, **kwargs):

        link_object = get_object_or_404(Binary_images_links, generated_uuid=kwargs['temp_link'])

        if timezone.now() < link_object.time_created + timezone.timedelta(seconds=link_object.life_time):
            return HttpResponse(link_object.image.binary_image)
        else:
            return Response({'response': "link's dead"})
