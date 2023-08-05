from django.urls import path
from .views import IndexView, PreviewDetail, PreviewList

app_name = 'autopost'

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('preview_list/', PreviewList.as_view(), name='preview_list'),
    path('preview_detail/', PreviewDetail.as_view(), name='preview_detail'),
]
