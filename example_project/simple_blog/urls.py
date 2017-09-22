from django.conf.urls import include, url
from django.contrib import admin
from .views import ArticleListView

admin.autodiscover()

urlpatterns = [
    url(r'^$', ArticleListView.as_view()),

    url(r'^admin/', include(admin.site.urls)),
]
