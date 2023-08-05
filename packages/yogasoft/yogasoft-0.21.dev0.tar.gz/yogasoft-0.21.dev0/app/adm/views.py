from ..forms import *
from ..models import *
from .custom import user_can_decorator
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import Permission
from django.core.urlresolvers import reverse
from django.db import transaction
from django.db.models import Q
from django.http import HttpResponseRedirect, StreamingHttpResponse
from django.shortcuts import redirect, render
from django.template import RequestContext
from django.views import View
from django.views.generic import (
    TemplateView, ListView,
    DetailView, FormView,
    CreateView, UpdateView,
    DeleteView
)
from django.utils.decorators import method_decorator
from shutil import rmtree
from mimetypes import MimeTypes
from os.path import join, abspath, getsize, exists
from os import mkdir, listdir, chdir, getcwd


import PIL.Image
from wsgiref.util import FileWrapper
from itertools import chain
import zipfile

TESTIMONIALS_ON_PAGE = 8
TESTIMONIALS_ON_ADMIN_PAGE = 8



class AccessRequired(TemplateView):
    template_name = 'access_required_page.html'


class AdminBlogPostCreate(CreateView):
    model = BlogPost
    form_class = CreateBlogForm
    template_name = "admin_blog_post_create.html"

    def post(self, request, *args, **kwargs):
        data = request.POST
        q = BlogPost(name=data['name'], text=data['text'], nameUA=data['nameUA'], textUA=data['textUA'],
                     author=User.objects.get(username=request.user))
        q.save()
        q.tags = []
        for i in request.POST.getlist('tags'):
            q.tags.add(Tag.objects.get(id=i))
        q.save()
        for i in request.FILES.getlist('file'):
            img = BlogPostImage(image=i, content=q)
            img.save()
        return redirect("/app/adm/blog")

class AdminBlogPostDelete(DeleteView):
    model = BlogPost
    success_url = "/app/adm/blog"
    template_name = 'admin_confirm_delete.html'

class AdminBlogPostDetail(DetailView):
    """ View that is responsible for blog page """
    model = BlogPost
    template_name = 'admin_blog_post_detail.html'

    def get_context_data(self, **kwargs):
        """ Method that collects all comments for current blog """
        context = super(AdminBlogPostDetail, self).get_context_data(**kwargs)
        blog_post = context['object']
        context['tags'] = blog_post.tags.all()
        comments = blog_post.comment_set.all()
        context['comments'] = {}
        for i in comments:
            if i.is_moderated:
                context['comments'][i] = list(CommentSecondLevel.objects.filter(father_comment=i))
                for j in context['comments'][i]:
                    if not j.is_moderated:
                        context['comments'][i].pop(context['comments'][i].index(j))
        context['form'] = CommentForm()
        context.pop('blogpost')
        return context

class AdminBlogPostEdit(UpdateView):
    model = BlogPost
    fields = ['name', 'nameUA', 'text', 'textUA', 'tags']
    template_name = "admin_blog_post_edit.html"
    success_url = "/app/adm/blog"

class AdminBlogPostList(ListView):
    model = BlogPost
    template_name = 'admin_blog_list.html'

    def get_context_data(self, **kwargs):
        context = super(AdminBlogPostList, self).get_context_data(**kwargs)
        return context

    def get_queryset(self):
        if 'tag' in self.kwargs:
            return Tag.objects.get(name__exact=self.kwargs['tag']).blogpost_set.all()
        else:
            return BlogPost.objects.all()



class AdminCommentDelete(View):
    @method_decorator(user_can_decorator(['comment_permission']), name='dispatch')
    def get(self, request, pk):
        q = Comment.objects.get(id=pk)
        q.delete()
        return HttpResponseRedirect(request.META['HTTP_REFERER'])

class AdminCommentSecDelete(View):
    @method_decorator(user_can_decorator(['comment_permission']), name='dispatch')
    def get(self, request, pk):
        q = CommentSecondLevel.objects.get(id=pk)
        q.delete()
        return HttpResponseRedirect(request.META['HTTP_REFERER'])

class AdminCommentModerate(View):
    @method_decorator(user_can_decorator(['comment_permission']), name='dispatch')
    def get(self, request, pk):
        q = Comment.objects.get(id=pk)
        q.is_moderated = True
        q.save()
        return HttpResponseRedirect(request.META['HTTP_REFERER'])

class AdminCommentSecModerate(View):
    @method_decorator(user_can_decorator(['comment_permission']), name='dispatch')
    def get(self, request, pk):
        q = CommentSecondLevel.objects.get(id=pk)
        q.is_moderated = True
        q.save()
        return HttpResponseRedirect(request.META['HTTP_REFERER'])

@method_decorator(user_can_decorator(['comment_permission']), name='dispatch')
class AdminCommentList(ListView):
    model = Comment
    template_name = 'admin_comment_list.html'
    context_object_name = 'comments'
    paginate_by = 20

    def get_queryset(self):
        if 'mod' in self.request.GET:
            view_moderated = self.request.GET['mod']
            if view_moderated == 'true':
                return list(chain(Comment.objects.filter(is_moderated=True).order_by('-id'),
                                  CommentSecondLevel.objects.filter(is_moderated=True).order_by('-id')))
            elif view_moderated == 'false':
                return list(chain(Comment.objects.filter(is_moderated=False).order_by('-id'),
                                  CommentSecondLevel.objects.filter(is_moderated=False).order_by('-id')))
            else:
                return list(
                    chain(Comment.objects.all().order_by('-id'), CommentSecondLevel.objects.all().order_by('-id')))
        else:
            return list(chain(Comment.objects.all().order_by('-id'), CommentSecondLevel.objects.all().order_by('-id')))



@method_decorator(user_can_decorator(['portfolio_permission']), name='dispatch')
class AdminPortfolioCreate(CreateView):
    model = PortfolioContent
    form_class = CreatePortfolio
    template_name = "admin_portfolio_create.html"

    @transaction.atomic
    def post(self, request, *args, **kwargs):

        data = request.POST
        q = PortfolioContent(name=data['name'], description=data['description'], nameUA=data['nameUA'],
                             descriptionUA=data['descriptionUA'], technologies=data['technologies'],
                             link=data['link'], client=data['client'])
        q.save()
        q.tags = []
        for i in request.POST.getlist('tags'):
            q.tags.add(Tag.objects.get(id=i))
        q.save()
        for i in request.FILES.getlist('file'):
            img = ImageContentClass(image=i, content=q)
            img.save()
        return redirect("/")

@method_decorator(user_can_decorator(['portfolio_permission']), name='dispatch')
class AdminPortfolioEdit(UpdateView):
    model = PortfolioContent
    fields = ['name', 'nameUA', 'description', 'descriptionUA', 'tags', "technologies", 'link', 'client']
    template_name = "admin_portfolio_edit.html"
    success_url = "/app/adm/portfolio"

@method_decorator(user_can_decorator(['portfolio_permission']), name='dispatch')
class AdminPortfolioDelete(DeleteView):
    model = PortfolioContent
    success_url = '/'
    template_name = "admin_confirm_delete.html"

@method_decorator(user_can_decorator(['portfolio_permission']), name='dispatch')
class AdminPortfolioDetail(DetailView):
    """02.03.2017 Taras this is detail portfolio view of concrete project"""
    model = PortfolioContent
    template_name = 'admin_portfolio_detail.html'

    def get_context_data(self, **kwargs):
        i = self.kwargs['pk']
        object = PortfolioContent.objects.get(pk=i)
        first_image = list(object.imagecontentclass_set.all())[0]
        next_images = list(object.imagecontentclass_set.all())[1:]

        return {'first_image': first_image, 'next_images': next_images, 'portfoliocontent': object}

@method_decorator(user_can_decorator(['portfolio_permission']), name='dispatch')
class AdminPortfolioList(ListView):
    model = PortfolioContent
    template_name = "admin_portfolio_list.html"



class AdminTestimonialList(ListView):
    model = Testimonial
    template_name = "admin_testimonial_list.html"
    paginate_by = TESTIMONIALS_ON_ADMIN_PAGE
    context_object_name = "testimonials"

    def get_queryset(self):
        if 'mod' in self.request.GET:
            view_moderated = self.request.GET['mod']
            if view_moderated == 'true':
                return Testimonial.objects.filter(is_moderated=True).order_by('-date')
            elif view_moderated == 'false':
                return Testimonial.objects.filter(is_moderated=False).order_by('-date')
            else:
                return Testimonial.objects.order_by('date')  # If not specified get all.
        else:
            return Testimonial.objects.order_by('date')  # If not specified get all.


    def post(self, request, testimonial_id=None):
        view_moderated = request.GET.get('mod', 'all')
        page = request.GET.get('page', 1)

        if 'moderated' in request.POST:
            try:
                testimonial = Testimonial.objects.get(pk=testimonial_id)
                testimonial.is_moderated = True
                testimonial.save()
            except Testimonial.DoesNotExist:
                return HttpResponseRedirect(reverse('app_admin:admin_testimonials') + '?mod={0}&page={1}'
                                            .format(view_moderated, page))
            return HttpResponseRedirect(reverse('app_admin:admin_testimonials') + '?mod={0}&page={1}'
                                        .format(view_moderated, page))

        elif 'delete' in request.POST:
            try:
                testimonial = Testimonial.objects.get(pk=testimonial_id)
                testimonial.delete()
            except Testimonial.DoesNotExist:
                return HttpResponseRedirect(reverse('app_admin:admin_testimonials') + '?mod={0}&page={1}'
                                            .format(view_moderated, page))
            return HttpResponseRedirect(reverse('app_admin:admin_testimonials') + '?mod={0}&page={1}'
                                        .format(view_moderated, page))

        elif 'save' in request.POST:
            author_name = request.POST['author_name']
            author_email = request.POST['author_email']
            message = request.POST['message']
            new_tstm = Testimonial(author_name=author_name, author_email=author_email, message=message)
            new_tstm.save()
            return HttpResponseRedirect(reverse('app_admin:admin_testimonials') + '?mod={0}&page={1}'
                                        .format(view_moderated, page))
        else:
            return HttpResponseRedirect(reverse('app_admin:admin_testimonials') + '?mod={0}&page={1}'
                                        .format(view_moderated, page))

class AdminProjectDelete(DeleteView):
    model = Project
    success_url = '/'
    template_name = "app/confirm_delete.html"

    def delete(self, request, *args, **kwargs):
        """
        Calls the delete() method on the fetched object and then
        redirects to the success URL.
        """
        self.object = self.get_object()
        success_url = self.get_success_url()
        try:
            rmtree(self.object.file)
        except FileNotFoundError:
            pass
        self.object.delete()
        return HttpResponseRedirect(success_url)



@method_decorator(user_can_decorator(['admin_users']), name='dispatch')
class AdminUser(ListView):
    model = User
    template_name = "admin_user_list.html"
    context_object_name = "users"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.login_used = False

    def get_queryset(self):
        return User.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['login_used'] = self.login_used
        self.login_used = False
        return context

    def post(self, request):
        if 'save' in request.POST:
            new_user = request.POST['username']
            if len(User.objects.filter(username=new_user)) > 0:  # Check if username is already used
                self.login_used = True
                return self.get(self, request)
            new_user = User(username=new_user)
            new_user.set_password(request.POST['password'])
            new_user.save()
            useryoga = UserYoga.objects.get(user=new_user)
            useryoga.is_admin = False
            useryoga.auth_by_sn = False
            useryoga.save()
            return HttpResponseRedirect(reverse('app_admin:admin_user_edit', args=(new_user.id,)))
        return self.get(self, request)

@method_decorator(user_can_decorator(['admin_users']), name='dispatch')
class AdminUserEdit(TemplateView):
    model = User
    template_name = "admin_user_edit.html"
    context_object_name = "user_obj"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.login_used = False

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            user_obj = User.objects.get(pk=self.kwargs['user_id'])
            context['user_obj'] = user_obj
            context['blog_admin'] = user_obj.has_perm('app.blog_admin')
            context['portfolio_admin'] = user_obj.has_perm('app.portfolio_admin')
            context['testimonials_admin'] = user_obj.has_perm('app.testimonials_admin')
            context['projects_admin'] = user_obj.has_perm('app.projects_admin')
            context['user_messages'] = user_obj.has_perm('app.user_messages')
            context['admin_users'] = user_obj.has_perm('app.admin_users')
            context['general_users'] = user_obj.has_perm('app.general_users')
            context['comments_admin'] = user_obj.has_perm('app.comments_admin')
            context['tags_admin'] = user_obj.has_perm('app.tags_admin')
            context['user_exist'] = True
            context['login_used'] = self.login_used
            self.login_used = False
        except User.DoesNotExist:
            context['user_exist'] = False
        return context

    def post(self, request, user_id=None):
        try:
            user_obj = User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return HttpResponseRedirect(reverse('app_admin:admin_user_list'))

        if 'change_pass' in request.POST:
            new_pass = request.POST['password']
            user_obj.set_password(new_pass)
            return HttpResponseRedirect(reverse('app_adm:admin_user_list'))

        elif 'delete' in request.POST:
            user_obj.delete()
            return HttpResponseRedirect(reverse('app_admin:admin_user_list'))

        elif 'save' in request.POST:
            new_username = request.POST['username']
            if len(User.objects.filter(~Q(pk=user_id), Q(username=new_username))) > 0:  # Check if login is already used
                self.login_used = True
                return self.get(request)
            user_obj.username = request.POST['username']
            user_obj.first_name = request.POST['first_name']
            user_obj.last_name = request.POST['last_name']
            user_obj.email = request.POST['email']
            perm_list = []
            for perm in ['blog_admin', 'portfolio_admin', 'testimonials_admin', 'projects_admin',
                         'user_messages', 'admin_users', 'general_users', 'comments_admin', 'tags_admin']:
                if perm in request.POST:
                    perm_list.append(Permission.objects.get(codename=perm))
            user_obj.user_permissions.set(perm_list)
            user_obj.save()
            return HttpResponseRedirect(reverse('app_admin:admin_user_list'))
        else:
            return HttpResponseRedirect(reverse('app_admin:admin_user_list'))

@method_decorator(user_can_decorator(['admin_users']), name='dispatch')
class AdminUserDelete(View):
    @method_decorator(user_can_decorator(['admin_users']), name='dispatch')
    def get(self, request, user_id):
        q = User.objects.get(id=user_id)
        q.delete()
        return HttpResponseRedirect(request.META['HTTP_REFERER'])


@method_decorator(user_can_decorator(['general_users']), name='dispatch')
class GeneralUsers(ListView):
                model = User
                template_name = "app/general_users.html"
                context_object_name = "users"

                def get_queryset(self):
                    return User.objects.filter(useryoga__is_admin=False)

                @staticmethod
                def post(self, request):
                    if 'save' in request.POST:
                        new_user = request.POST['username']
                        if len(User.objects.filter(username=new_user)) > 0:  # Check if username is already used
                            return HttpResponseRedirect(reverse('app:admin_users'))
                        new_user = User(username=new_user)
                        new_user.set_password(request.POST['password'])
                        new_user.save()
                        useryoga = UserYoga.objects.get(user=new_user)
                        useryoga.is_admin = True
                        useryoga.auth_by_sn = False
                        useryoga.save()
                        return HttpResponseRedirect(reverse('app:edit_admin_user', args=(new_user.id,)))
                    return HttpResponseRedirect(reverse('app:admin_users'))


# @method_decorator(user_can_decorator(['custom_permission_1']), name='dispatch')  # Decorator use example
class MainPage(TemplateView):
    template_name = 'base.html'


class ProjectDetailView(DetailView):
    model = Project
    template_name = "app/project_view.html"

    def get_context_data(self, **kwargs):
        """
        Insert the single object into the context dict.
        """
        context = {}
        if self.object:
            context['object'] = self.object
            context_object_name = self.get_context_object_name(self.object)
            if context_object_name:
                context[context_object_name] = self.object
            try:
                context['files'] = [join(str(i)) for i in listdir(self.object.file)]
            except FileNotFoundError:
                context['files'] = ['There is no files']
        context.update(kwargs)
        return super(ProjectDetailView, self).get_context_data(**context)


class ProjectsListView(ListView):
    model = Project
    template_name = "app/projects_list.html"



class SiteAdmin(TemplateView):
    template_name = 'site_admin.html'

    def get_context_data(self, **kwargs):
        context = dict()
        context['new_comments'] = len(Comment.objects.filter(is_moderated=False)) + \
                                  len(CommentSecondLevel.objects.filter(is_moderated=False))
        context['new_testimonials'] = len(Testimonial.objects.filter(is_moderated=False))
        context['opened_projects'] = len(Project.objects.filter(is_opened=True))
        context['new_feedback'] = len(ContactUsModel.objects.filter(is_new=True))
        return context




def project_file_download(request, pk, file):
    pth = Project.objects.get(id=pk).file
    back = getcwd()
    chdir(pth)
    mime = MimeTypes()
    resp = StreamingHttpResponse(FileWrapper(open(file, 'rb'), 8192), content_type=mime.guess_type(url=file))
    resp['Content-Length'] = getsize(file)
    resp["Content-Disposition"] = "attachment; filename=" + file
    chdir(back)
    return resp


def project_all_files_download(request, pk):
    pth = Project.objects.get(id=pk).file
    back = getcwd()
    chdir(pth)
    files = listdir(pth)
    zip_filename = "".join(("project", str(pk), ".zip"))
    if not exists(zip_filename):
        with zipfile.ZipFile(zip_filename, "w") as zf:
            for i in files:
                zf.write(str(i))

    resp = StreamingHttpResponse(FileWrapper(open(zip_filename, 'rb'), 8192), content_type="application/zip-file")
    resp['Content-Length'] = getsize(zip_filename)
    resp["Content-Disposition"] = "attachment; filename=" + zip_filename
    chdir(back)
    return resp



def close_project(request, pk):
    z = Project.objects.get(id=pk)
    z.is_opened = False
    z.save()
    return HttpResponseRedirect(request.META['HTTP_REFERER'])


class SearchListAsView(ListView):
    """ this class is responsible for search

    It searchs blog posts on info that user inputs, It uses Ajax queries
    """
    template_name = 'app/ajax_list_view.html'
    model = BlogPost

    def get_context_data(self, **kwargs):
        context = super(SearchListAsView, self).get_context_data(**kwargs)
        # here we can add some additional context
        context.update({
            'tag_list': None,
        })
        return context

    def get_queryset(self):
        return BlogPost.objects.filter(Q(name__contains=self.kwargs['info']) | Q(text__contains=self.kwargs['info']))


