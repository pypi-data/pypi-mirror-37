from . import views
from django.conf.urls import url
from django.views.decorators.cache import cache_page

app_name = 'app'
urlpatterns = [

    url(r'^$', views.IndexPage.as_view(), name="main_page"),

    url(r'^blog/$', views.BlogListView.as_view(), name='blog_list_view'),
    url(r'^blog/(?P<pk>\d+)/add_comment/$', views.add_comment, name='add_comment'),
    url(r'^blog/(?P<pk>\d+)/add_comment/(?P<comm_pk>\d+)/$', views.add_second_comment, name='add_second_level_comment'),
    url(r'^blog/(?P<pk>\d+)/$', cache_page(5)(views.BlogPostDetailView.as_view()), name='blog_detail_view'),
    url(r'^blog/tag/(?P<tag>[a-zA-Z0-9\s]+)/$', views.BlogListView.as_view(), name='blog_list_view_tag'),

    url(r'^contact_us/$', views.ContactUsView.as_view(), name='contact_us'),

    url(r'index/$', views.IndexPage.as_view(), name="index_page"),

    url(r'^logout/$', views.user_logout, name='logout'),

    url(r'^portfolio/$', views.PortfolioListView.as_view(), name="portfolio"),
    url(r'^portfolio/(?P<pk>\d+)', views.PortfolioDetailView.as_view(), name="portfolio_detail"),

    url(r'^registration$', views.register, name="registration"),

    url(r'^search_list/(?P<info>.*)$', views.SearchListAsView.as_view(), name='search'),
    url(r'start_project/$', views.StartProjectView.as_view(), name="start_project"),

    url(r'testimonials/$', views.TestimonialsListView.as_view(), name="testimonials_list_view"),






]
