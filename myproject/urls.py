
from django.contrib import admin
from django.urls import path
from myproject.views import *
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('home/', home,name='home'),
    path('base/', base,name='base'),
    path('', loginPage,name='loginPage'),
    path('register/', register,name='register'),
    path('logoutpage/', logoutPage,name='logoutpage'),
    path('joobfeed/', joobfeed,name='joobfeed'),
    path('addjob/', addjob,name='addjob'),
    path('apply_now/<str:apply_id>', apply_now,name='apply_now'),
    path('changePassword/', changePassword, name='changePassword'),
 
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
