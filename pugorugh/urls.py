from django.conf.urls import url
from django.views.generic import TemplateView
from django.views.generic.base import RedirectView

from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework.authtoken.views import obtain_auth_token

from pugorugh.views import (
    UserRegisterView, DogListView, DogDetailView, SeeUpdatePreferencesView,
    NextDog, RatedDog
)

# API endpoints
urlpatterns = format_suffix_patterns([
    url(r'^api/user/login/$', obtain_auth_token, name='login-user'),
    url(r'^api/user/$', UserRegisterView.as_view(), name='register-user'),
    url(r'^favicon\.ico$',
        RedirectView.as_view(
            url='/static/icons/favicon.ico',
            permanent=True
        )),
    url(r'^$', TemplateView.as_view(template_name='pugorugh/index.html')),
    url(r'^api/dogs/$', DogListView.as_view(), name='all_dogs'),
    url(
        r'^api/dogs/(?P<filter>[a-z]+)/$',
        DogListView.as_view(),
        name='filtered_dogs'
    ),
    url(r'api/dog/(?P<pk>\d+)/$', DogDetailView.as_view(), name='dog'),
    url(
        r'api/dog/(?P<pk>\d+)/(?P<rating>[a-z]+)/next/$',
        NextDog.as_view(),
        name="next_dog",
    ),
    url(
        r'api/dog/(?P<pk>\d+)/(?P<rating>[a-z]+)/$',
        RatedDog.as_view(),
        name="rated_dog",
    ),
    url(r'api/user/preferences/$', SeeUpdatePreferencesView.as_view(),
        name="update_preferences"),
])
