from django.urls import path
from .views import SnippetList, Analysis2List

urlpatterns = [
    path('', SnippetList.as_view(), name='json_request'),
    path('2/', Analysis2List.as_view(), name='form_request'),
]
