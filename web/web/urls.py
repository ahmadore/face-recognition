from django.conf.urls import url
from django.contrib import admin
from recognition import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', views.index),
    url(r'^report/$', views.report),
    url(r'^find/$', views.find),
    url(r'^api/find$', views.find_api),
    url(r'^api/report$', views.report_api)
] \
+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
# + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
