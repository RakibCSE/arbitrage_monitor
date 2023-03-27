from django.conf.urls import url, include
from django.contrib import admin
from django.contrib.auth import views

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^', include('base.urls')),

    # django allauth package url
    # url(r'^accounts/logout/$', views.logout, {'next_page': '/'}),
    url(r'^accounts/logout/$', views.logout, {'next_page': settings.LOGOUT_REDIRECT_URL}, name='logout'),
    url(r'^accounts/', include("allauth.urls")),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
if settings.DEBUG:
    import debug_toolbar

    urlpatterns = [
                      url(r'^__debug__/', include(debug_toolbar.urls)),
                  ] + urlpatterns
