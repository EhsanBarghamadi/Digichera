from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('page.urls', namespace='page')),
    path('user/', include('user.urls', namespace='user')),
    path('account/', include('account.urls', namespace='account')),
]
