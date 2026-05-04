from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.sitemaps.views import sitemap
from users import views
from users.sitemaps import StaticViewSitemap, ServiceSitemap, ProviderSitemap


sitemaps = {
    'static': StaticViewSitemap(),
    'services': ServiceSitemap(),
    'providers': ProviderSitemap(),
}


urlpatterns = [
    path('admin/', admin.site.urls),

    path('', views.home, name='home'),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='sitemap'),

    path('accounts/', include('allauth.urls')),
    path('', include('users.urls')),
    path('jobs/', include('jobs.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)