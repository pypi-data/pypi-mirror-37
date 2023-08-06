import uuid

from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.core.paginator import Paginator
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.http import HttpResponse, JsonResponse
from django.utils.text import slugify
from django.utils import timezone

from .models import Post
from .mixins import AuthorRequiredMixin
from .settings import settings as app_settings

common_context = {
    'settings': app_settings
}


class BlogHomeView(View):
    
    def get(self, request):
        posts_list = Post.objects.filter(is_deleted=False, is_published=True)
        paginator = Paginator(posts_list, 15)

        page = request.GET.get('page')
        posts = paginator.get_page(page)
        return render(request, 'django-blogs/home.html', {
            'posts': posts,
            **common_context,
        })

class NewBlogView(LoginRequiredMixin, AuthorRequiredMixin, View):

    def get(self, request):
        post = Post.objects.create(
            author=request.user.username,
            uuid=uuid.uuid4(),
            heading="Click to edit Title",
            content="<p>Click to edit body</p>"
        )
        return redirect('blogs:edit', uuid=post.uuid)

class BlogEditView(LoginRequiredMixin, AuthorRequiredMixin, View):

    def get(self, request, uuid):
        post = get_object_or_404(Post, pk=uuid)
        if not post.author == request.user.username:
            raise PermissionDenied
        return render(request, 'django-blogs/editor.html', {
            'blog': post,
            **common_context,
        })
    
    def post(self, request, uuid):
        if not all([key in request.POST for key in ['heading', 'content']]):
            return JsonResponse(
                {
                    'error': "'heading' and 'content' required"
                },
                status=400)
        post = get_object_or_404(Post, pk=uuid)
        if not post.author == request.user.username:
            raise PermissionDenied
        post.heading = request.POST['heading']
        post.slug = '-'.join([
            slugify(request.POST['heading'])[:200],
            post.uuid.hex[:12]
        ])
        post.content = request.POST['content']
        post.save()
        return HttpResponse(status=200)

class BlogDraftView(LoginRequiredMixin, AuthorRequiredMixin, View):

    def get(self, request):
        posts_list = Post.objects.filter(
            author__exact=request.user.username,
            is_deleted=False,
            is_published=False)
        paginator = Paginator(posts_list, 15)

        page = request.GET.get('page')
        posts = paginator.get_page(page)
        return render(request, 'django-blogs/drafts.html', {
            'posts': posts,
            **common_context,
        })

class BlogReadView(View):

    def get(self, request, slug):
        post = get_object_or_404(
            Post,
            slug=slug,
            is_deleted=False,
            is_published=True)
        return render(request, 'django-blogs/blog.html', {
            'post': post,
            **common_context
        })

class BlogPublishView(LoginRequiredMixin, AuthorRequiredMixin, View):

    def get(self, request, uuid):
        post = get_object_or_404(Post, pk=uuid)
        if not post.author == request.user.username:
            raise PermissionDenied
        post.is_published = True
        post.published_on = timezone.now()
        post.slug = '-'.join([
            slugify(post.heading)[:200],
            post.uuid.hex[:12]
        ])
        post.save()
        return redirect("blogs:read", slug=post.slug)

class BlogDeleteView(LoginRequiredMixin, AuthorRequiredMixin, View):

    def get(self, request, uuid):
        post = get_object_or_404(Post, pk=uuid)
        if not post.author == request.user.username:
            raise PermissionDenied
        post.is_deleted = True
        post.save()
        return redirect("blogs:home")