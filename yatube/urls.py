from django.contrib import admin
from django.contrib.flatpages import views
from django.urls import path, include
from django.conf import settings
from django.conf.urls import handler404, handler500
from django.conf.urls.static import static

handler404 = 'posts.views.page_not_found'
handler500 = 'posts.views.server_error'

urlpatterns = [
    path('', include('users.urls')),
    path('about/', include('django.contrib.flatpages.urls')),
    path('auth/', include('django.contrib.auth.urls')),
    path('admin/', admin.site.urls),
    path('', include('posts.urls')),
]

urlpatterns += [
    path('about-us/', views.flatpage, {'url': '/about-us/'}, name='about'),
    path('terms/', views.flatpage, {'url': '/terms/'}, name='terms'),
    path('about-author/', views.flatpage,
         {'url': '/about-author/'}, name='auth'),
    path('about-spec/', views.flatpage, {'url': '/about-spec/'}, name='spec'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)
