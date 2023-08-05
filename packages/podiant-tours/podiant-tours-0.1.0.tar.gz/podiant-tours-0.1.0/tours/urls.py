from django.conf.urls import url
from django.contrib.auth.decorators import login_required
from .views import TourDataView


urlpatterns = [
    url(
        r'^tours\.js$',
        login_required(TourDataView.as_view()),
        name='tour_data'
    )
]
