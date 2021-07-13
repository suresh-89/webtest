from django.conf.urls import url
from . import views

from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView,LogoutView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # post views
    url(r'^$', views.post_list, name='post_list'),
    url(r'^tag/(?P<tag_slug>[-\w]+)/$', views.post_list, name='post_list_by_tag'),
    #url(r'^$', views.PostListView.as_view(), name='post_list'),
    url(r'^(?P<year>\d{4})/(?P<month>\d{2})/(?P<day>\d{2})/(?P<post>[-\w]+)/$',
        views.post_detail,
        name='post_detail'),

    url(r'^search/$', views.post_search, name='post_search'),
    #new
    url(r'^login/$',  LoginView.as_view(
            template_name='blog/post/login.html',extra_context={'next': '/blog/'}
        ),
        name='mysite_login'),
    url(r'^signup/$', views.signup, name='mysite_signup'),
    url(r'^logout/$', LogoutView.as_view(), name="mysite_logout"),
]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns+=static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    urlpatterns = urlpatterns + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
