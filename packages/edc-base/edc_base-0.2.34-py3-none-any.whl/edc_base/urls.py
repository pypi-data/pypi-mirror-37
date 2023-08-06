from django.urls.conf import path

from edc_base.views import HomeView

app_name = 'edc_base'

urlpatterns = [
    path(r'', HomeView.as_view(), name='home_url'),
]
