from django.contrib import admin
from django.urls import path, include
from account import views
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name = 'index'),
    path('account/', include('account.urls')),
    path('social-auth/', include('social_django.urls', namespace = 'social')),
    path('images/', include('images.urls', namespace = 'images')),

]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root = settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
