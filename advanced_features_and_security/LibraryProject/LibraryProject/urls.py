from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from relationship_app.views import home

urlpatterns = [
    path('', home, name='home'),
    path('admin/', admin.site.urls),
    path('relationship/', include('relationship_app.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


