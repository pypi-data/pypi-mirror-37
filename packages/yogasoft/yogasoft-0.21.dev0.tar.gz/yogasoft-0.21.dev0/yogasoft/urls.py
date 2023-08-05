from django.conf.urls import url, include
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic.base import RedirectView

urlpatterns = [
    url(r'^$', RedirectView.as_view(url='/app/index', permanent=False), name="main_page"),

    #url(r'^activate/(?P<key>.+)$', activation, name='activation'),
    url('^accounts/', include('django.contrib.auth.urls')),
    url('', include('social_django.urls', namespace='social')),
    url(r'^admin/', admin.site.urls),
    url(r'^app/', include("app.urls")),
    url(r'^app/adm/', include("app.adm.urls", namespace='app_admin')),

    url(r'^i18n/', include('django.conf.urls.i18n')),
    url(r'^s3direct/', include('s3direct.urls')),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
