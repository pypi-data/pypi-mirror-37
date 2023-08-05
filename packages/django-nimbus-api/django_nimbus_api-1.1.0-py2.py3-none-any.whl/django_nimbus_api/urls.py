from django.conf import settings
from django.conf.urls import url, include

from .views import get_swagger_view

urlpatterns = [
    url(r'^$', get_swagger_view()),
]
