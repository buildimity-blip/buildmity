from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static


def home(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    return redirect('login')


from django.shortcuts import redirect

urlpatterns = [
    path('', home, name='home'),
    path('admin/', admin.site.urls),

    path('accounts/', include('allauth.urls')),
    path('', include('users.urls')),
    path('jobs/', include('jobs.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)