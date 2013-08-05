from django.conf.urls import patterns, include, url
from django.contrib import admin
from .views import ArticleListView

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', ArticleListView.as_view()),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)
