from django.contrib import admin
from django.urls import path, include
from relationship_app.views import home

urlpatterns = [
    path('', home, name='home'),
    path('admin/', admin.site.urls),
    path('relationship/', include('relationship_app.urls')),
]




