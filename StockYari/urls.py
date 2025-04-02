from django.contrib import admin
from django.urls import path,include

urlpatterns = [
    path('manage-admin/', admin.site.urls),
    path('api/v1/', include('app.urls')),
]
