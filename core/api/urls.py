from django.urls import path, include
from api.views import ImageAPIViewSet, TempLinkAPI


urlpatterns = [
    path('auth/', include('rest_framework.urls')),
    path('image_list/', ImageAPIViewSet.as_view({'get': 'list'})),
    path('image_upload/', ImageAPIViewSet.as_view({'post': 'create'})),
    path('link_generate/', TempLinkAPI.as_view({'post': 'create'})),
    path('link_list/', TempLinkAPI.as_view({'get': 'list'})),
    path('<str:temp_link>/', TempLinkAPI.as_view({'get': 'retrieve'})),
]
