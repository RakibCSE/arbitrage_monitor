from django.conf.urls import url
from django.conf.urls.static import static
from django.conf import settings
from . import views

app_name = "base"

urlpatterns = [
                  url(r'^$', views.index, name='home'),
                  url(r'^update/$', views.edit_profile, name='update'),
                  url(r'^about/$', views.about, name='about'),
                  url(r'^(?P<id>[0-9]+)/profile/$', views.show_profile, name='profile'),
                  url(r'^cryptocurrencies/$', views.show_all_cryptocurrencies, name='cryptocurrencies'),

                  # allauth login and signup override
                  url(r'^accounts/login/$', views.MyLoginView.as_view(), name='login'),
                  url(r'^accounts/signup/', views.MySignupView.as_view(), name='register'),

              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
