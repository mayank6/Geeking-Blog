from django.urls import path,re_path,include
from django.contrib import admin
from django.contrib.sitemaps.views import sitemap

from .views import(
	blog_home,
	blog_create,
	blog_delete,
	blog_update,
	blog_detail,
	BlogSitemap,
	tag_view,
	
	)
sitemaps = {
    'static': BlogSitemap,
}
app_name='posts'
urlpatterns=[
   path('',blog_home,name="home"),
   path('create/',blog_create,name='create'),
   re_path(r'^(?P<slug>[\w-]+)/edit/$',blog_update,name='update'),
   re_path(r'^(?P<slug>[\w-]+)/delete/$',blog_delete,name='delete'),
   re_path(r'^(?P<slug>[\w-]+)/$',blog_detail,name='detail'),
   path('sitemap.xml', sitemap, {'sitemaps': sitemaps},
         name='django.contrib.sitemaps.views.sitemap'),
   re_path(r'^tag/(?P<slug>[\w-]+)/$',tag_view,name='tag_view')
   


]