from . import views
from django.conf.urls import url
from django.contrib.auth.decorators import login_required, permission_required
from django.views.decorators.cache import cache_page, never_cache


urlpatterns = [

    url(r'^$', views.SiteAdmin.as_view(), name='admin_main'),

    url(r'^access_required/$', views.AccessRequired.as_view(), name='access_required_page'),

    url(r'^user/$', never_cache(views.AdminUser.as_view()), name='admin_user_list'),
    url(r'^user/delete/(?P<user_id>[0-9]+)/$', never_cache(views.AdminUserDelete.as_view()), name='admin_user_delete'),
    url(r'^user/edit/(?P<user_id>[0-9]+)/$', views.AdminUserEdit.as_view(), name='admin_user_edit'),

    url(r'^blog/$', views.AdminBlogPostList.as_view(), name='admin_blog_post_list'),
    url(r'^blog/create/$', views.AdminBlogPostCreate.as_view(), name='admin_blog_post_create'),
    url(r'^blog/delete/(?P<pk>\d+)/$', views.AdminBlogPostDelete.as_view(), name='admin_blog_post_delete'),
    url(r'^blog/(?P<pk>\d+)', views.AdminBlogPostDetail.as_view(), name="admin_blog_post_detail"),
    url(r'^blog/edit/(?P<pk>\d+)/$', views.AdminBlogPostEdit.as_view(), name='admin_blog_post_edit'),
    url(r'^blog/tag/(?P<tag>[a-zA-Z0-9\s]+)/$', views.AdminBlogPostList.as_view(), name='admin_blog_list_view_tag'),

    url(r'^comments/$', never_cache(views.AdminCommentList.as_view()), name='admin_comment_list'),
    url(r'^comments/delete/(?P<pk>\d+)/$', never_cache(views.AdminCommentDelete.as_view()), name='admin_comment_delete'),
    url(r'^comments/delete_sec/(?P<pk>\d+)/$', never_cache(views.AdminCommentSecDelete.as_view()), name='admin_comment_delete_sec'),
    url(r'^comments/moderate/(?P<pk>\d+)/$', never_cache(views.AdminCommentModerate.as_view()), name='admin_comment_moderate'),
    url(r'^comments/moderate_sec/(?P<pk>\d+)/$', never_cache(views.AdminCommentSecModerate.as_view()), name='admin_comment_moderate_sec'),

    url(r'^portfolio/$', cache_page(5)(views.AdminPortfolioList.as_view()), name='admin_portfolio_list'),
    url(r'^portfolio/create/$', views.AdminPortfolioCreate.as_view(), name='admin_portfolio_create'),
    url(r'^portfolio/delete/(?P<pk>\d+)/$', views.AdminPortfolioDelete.as_view(), name='admin_portfolio_delete'),
    url(r'^portfolio/edit/(?P<pk>\d+)/$', views.AdminPortfolioEdit.as_view(), name='admin_portfolio_edit'),
    url(r'^portfolio/(?P<pk>\d+)', views.AdminPortfolioDetail.as_view(), name="admin_portfolio_detail"),


    url(r'^projects/$', views.ProjectsListView.as_view(), name='admin_projects_list'),
    url(r'^projects/(?P<pk>\d+)/$', views.ProjectDetailView.as_view(), name='project_view'),
    url(r'^projects/(?P<pk>\d+)/close/$', views.close_project, name='close_project'),
    url(r'^projects/(?P<pk>\d+)/delete/$', views.AdminProjectDelete.as_view(), name='admin_project_delete'),
    url(r'^projects/(?P<pk>\d+)/download/all/$', views.project_all_files_download, name='project_files_download'),
    url(r'^projects/(?P<pk>\d+)/download/(?P<file>\S+)/$', views.project_file_download,    name='project_file_download'),

    url(r'testimonials_admin/$', cache_page(5)(views.AdminTestimonialList.as_view()), name="admin_testimonials"),
    url(r'testimonials_admin/(?P<testimonial_id>[0-9]+)/$', cache_page(5)(views.AdminTestimonialList.as_view()),
        name="admin_testimonial_detail"),

]
