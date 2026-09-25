from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from store import views as store_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(('store.urls', 'store'), namespace='store')),
    
    # Global fallbacks for un-namespaced template calls
    path('cart/add/<int:product_id>/', store_views.cart_add, name='cart_add'),
    path('logout/', store_views.user_logout, name='logout'),
    path('login/', store_views.user_login, name='login'),
    path('signup/', store_views.user_signup, name='signup'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)