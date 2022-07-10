from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('watch_list.api.urls')),
    path('',include('user_app.api.urls')),
    path('api-auth/', include('rest_framework.urls')),
]
