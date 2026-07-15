from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('page.urls', namespace='page')),
    path('user/', include('user.urls', namespace='user')),
    path('account/', include('account.urls', namespace='account')),
    path('store/', include('store.urls', namespace='store')),
    path('products/', include('product.urls', namespace='product')),
    path('order/', include('order.urls', namespace='order')),
    path('cart/', include('cart.urls', namespace='cart')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
