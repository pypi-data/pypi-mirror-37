import logging
import PIL.Image
import zipfile

from app.forms import *
from app.models import *
from datetime import date, datetime
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Permission
from django.core.mail import send_mail
from django.core.urlresolvers import reverse
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.http import StreamingHttpResponse
from django.shortcuts import redirect, render
from django.template import RequestContext
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView, ListView, DetailView, FormView, CreateView, UpdateView, DeleteView
from itertools import chain
from mimetypes import MimeTypes
from os import mkdir, listdir, chdir, getcwd
from os.path import join, abspath, getsize, exists
from shutil import rmtree
from yogasoft.settings import EMAIL_HOST_USER
from wsgiref.util import FileWrapper




TESTIMONIALS_ON_PAGE = 8
TESTIMONIALS_ON_ADMIN_PAGE = 8


class BlogPostDetailView(DetailView):
    """ View that is responsible for blog page """
    model = BlogPost
    template_name = 'app/blog_post_detail.html'

    def get_context_data(self, **kwargs):
        """ Method that collects all comments for current blog """

        context = super(BlogPostDetailView, self).get_context_data(**kwargs)
        blog_post = context['object']
        context['tags'] = blog_post.tags.all()
        comments = blog_post.comment_set.all()
        context['comments'] = {}
        for i in comments:
            if i.is_moderated:
                context['comments'][i] = list(CommentSecondLevel.objects.filter(father_comment=i, is_moderated=True))
        context['form'] = CommentForm()
        context.pop('blogpost')
        return context


class BlogListView(ListView):
    """ View that is responsible for blog list page """
    model = BlogPost
    template_name = 'app/blog_list_view.html'

    def get_context_data(self, **kwargs):
        context = super(BlogListView, self).get_context_data(**kwargs)
        return context

    def get_queryset(self):
        if 'tag' in self.kwargs:
            return Tag.objects.get(name__exact=self.kwargs['tag']).blogpost_set.all()
        else:
            return BlogPost.objects.all()


class IndexPage(FormView):
    """ View that is responsible for main page """
    template_name = 'app/index.html'
    form_class = StartProjectForm
    success_url = '/'

    def post(self, request, *args, **kwargs):
        """ Post method that handles files, when user starts new project """
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        files = request.FILES.getlist('file')

        if form.is_valid():
            data = form.cleaned_data
            pth = join('stor', str(date.today()) + '-' + data['first_name'] + '-' + data['last_name'])
            try:
                mkdir(pth)
            except FileExistsError:
                pass
            form.cleaned_data['file'] = abspath(pth)
            for f in files:
                if str(f).endswith('.exe'):
                    continue
                with open(join(pth, str(f)), 'wb+') as destination:
                    for chunk in f.chunks():
                        destination.write(chunk)
            return self.form_valid(form, abspath(pth))
        else:
            return self.form_invalid(form)

    def form_valid(self, form, pth):
        a = form.save(commit=False)
        a.file = pth
        a.save()
        return super(IndexPage, self).form_valid(form)


class LoginPage(TemplateView):
    template_name = 'app/login_page.html'

# @method_decorator(user_can_decorator(['custom_permission_1']), name='dispatch')  # Decorator use example
class MainPage(TemplateView):
    template_name = 'base.html'


class PortfolioDetailView(DetailView):
    """02.03.2017 Taras this is detail portfolio view of concrete project"""
    model = PortfolioContent
    template_name = 'app/portfolio_detail_view.html'

    def get_context_data(self, **kwargs):
        i = self.kwargs['pk']
        object = PortfolioContent.objects.get(pk=i)
        first_image = list(object.imagecontentclass_set.all())[0]
        next_images = list(object.imagecontentclass_set.all())[1:]
        return {'first_image': first_image, 'next_images': next_images,
                'portfoliocontent': object, 'time': datetime.now().second}


class PortfolioListView(ListView):
    """02.03.2017 Taras  this list returns all Portfolio projects of our agency """
    template_name = 'app/portfolio_list.html'

    # paginate_by = 4

    def get_queryset(self):
        return PortfolioContent.objects.all().order_by('-id')


class SearchListAsView(ListView):
    """ this class is responsible for search

    It searchs blog posts and portfolio info that user inputs, It uses Ajax queries
    """
    template_name = 'app/ajax_list_view.html'

    def get_context_data(self, **kwargs):
        context = super(SearchListAsView, self).get_context_data(**kwargs)
        # here we can add some additional context
        context.update({
            'tag_list': None,
        })
        return context

    def get_queryset(self):
        blog_posts = BlogPost.objects.filter(Q(name__contains=self.kwargs['info']) | Q(text__contains=self.kwargs['info']))
        portfolio_content = PortfolioContent.objects.filter(Q(name__contains=self.kwargs['info'])
                                                     | Q(nameUA__contains=self.kwargs['info'])
                                                     | Q(description__contains=self.kwargs['info'])
                                                     | Q(descriptionUA__contains=self.kwargs['info']))

        return list(chain(blog_posts, portfolio_content))


class StartProjectView(FormView):
    template_name = "base.html"

class TestimonialsListView(ListView):
    """ View that is responsible for testimonials page """
    model = Testimonial
    template_name = "app/testimonials_list_view.html"
    paginate_by = TESTIMONIALS_ON_PAGE
    context_object_name = "testimonials"

    def get_queryset(self):
        return Testimonial.objects.filter(is_moderated=True).order_by('-date')

    def post(self, request):
        if 'save' in request.POST:
            author_name = request.POST['author_name']
            author_email = request.POST['author_email']
            message = request.POST['message']
            new_tstm = Testimonial(author_name=author_name, author_email=author_email, message=message)
            new_tstm.save()
            return HttpResponseRedirect(reverse('app:testimonials_list_view'))
        return HttpResponseRedirect(reverse('app:testimonials_list_view'))
















def add_comment(request, pk):
    """ Function that handles comment adding """

    data = request.POST
    if request.user.is_authenticated():
        q = Comment(author_email=request.user.email, author_name=request.user)
    else:
        q = Comment(author_email=data['author_email'], author_name=data['author_name'])
    q.message = data['message']
    q.blog = BlogPost.objects.get(pk=pk)

    if request.user.is_staff:  # if admin2, no need for other admin2 to moderate
        q.is_moderated = True
    q.save(q)

    send_mail(
        'New comment',
        data['message'],
        EMAIL_HOST_USER,
        ['codertarasvaskiv@gmail.com'],
        fail_silently=False,
    )
    return redirect('app:blog_detail_view', pk)


def add_second_comment(request, pk, comm_pk):
    """ Function that handles second level comment adding """

    data = request.POST
    if request.user.is_authenticated():
        q = CommentSecondLevel(author_email=request.user.email, author_name=request.user)
    else:
        q = CommentSecondLevel(author_email=data['author_email'], author_name=data['author_name'])
    q.message = data['message']
    q.father_comment = Comment.objects.get(pk=comm_pk)
    if request.user.is_staff:  # if admin2, no need for other admin2 to moderate
        q.is_moderated = True
    q.save(q)
    return redirect('app:blog_detail_view', pk)




@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/')


class ContactUsView(FormView):
    """ View that is responsible for feedback page """
    template_name = 'app/contact_us.html'
    form_class = ContactUsForm
    success_url = "/"

    def post(self, request, *args, **kwargs):
        data = request.POST
        q = ContactUsModel()
        q.author_email = data['author_email']
        q.author_name = data['author_name']
        q.message = data['message']
        q.save(q)
        return redirect("app:index_page")


def user_login(request):
    context = RequestContext(request)
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return render(request, '/', {}, context)
            else:
                return render(request, '/', {}, context)
        else:
            print("Invalid login details: {}, {}".format(username, password))
            return render(request, '/', {})
    else:
        return render(request, '/', {}, context)




def register(request):  # 06.03.2017 Taras need to edit later
    context = RequestContext(request)
    registered = False
    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        yoga_form = YogaUserForm(data=request.POST)

        if user_form.is_valid() and yoga_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()
            profile = yoga_form.save(commit=False)
            profile.user = user
            registered = True
        else:
            print(user_form.errors, yoga_form.errors)
    else:
        user_form = UserForm()
        yoga_form = YogaUserForm()
    return render(request, 'registration/registration_form.html', {'user_form': user_form, 'profile_form': yoga_form,
                                                                   'registered': registered}, context)




class CreateBlogPost(CreateView):
    model = BlogPost
    form_class = CreateBlogForm
    template_name = "app/create_blog_post.html"

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
        return redirect("/")





class ProjectsListView(ListView):
    model = Project
    template_name = "app/projects_list.html"


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


class ProjectDelete(DeleteView):
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




class CommentsAdmin(ListView):
    model = Comment
    template_name = 'app/comments_admin.html'
    context_object_name = 'comments'
    paginate_by = 10

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


def moderate_comment(request, pk):
    q = Comment.objects.get(id=pk)
    q.is_moderated = True
    q.save()
    return HttpResponseRedirect(request.META['HTTP_REFERER'])


def moderate_sec_comment(request, pk):
    q = CommentSecondLevel.objects.get(id=pk)
    q.is_moderated = True
    q.save()
    return HttpResponseRedirect(request.META['HTTP_REFERER'])


def delete_comment(request, pk):
    q = Comment.objects.get(id=pk)
    q.delete()
    return HttpResponseRedirect(request.META['HTTP_REFERER'])


def delete_sec_comment(request, pk):
    q = CommentSecondLevel.objects.get(id=pk)
    q.delete()
    return HttpResponseRedirect(request.META['HTTP_REFERER'])
