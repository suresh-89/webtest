from django.conf.urls import include, url
from django.contrib import admin




urlpatterns = [
    #url(r'^admin/', include(admin.site.urls)),
    url(r'^admin/', admin.site.urls),
    #url(r'^blog/', include('blog.urls', namespace='blog', app_name='blog')),
    url(r'^blog/', include(('blog.urls','blog'), namespace='blog')),

]

admin.site.site_url = None
