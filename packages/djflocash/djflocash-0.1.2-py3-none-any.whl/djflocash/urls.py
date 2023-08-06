from django.conf.urls import url
from django.conf import settings


from .views import NotificationReceive


urlpatterns = [
    url(
        r'^notification/%s/$' % settings.FLOCASH_NOTIFICATION_TOKEN,
        NotificationReceive.as_view(),
        name='notification_receive',
    ),
]
