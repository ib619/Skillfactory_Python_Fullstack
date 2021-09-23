from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Post

from django.views import View
from django.core.paginator import Paginator
from .filters import PostFilter
from .forms import PostForm

from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.shortcuts import render


class PostList(ListView):
    model = Post
    template_name = 'posts.html'
    context_object_name = 'posts'
    ordering = ['-id']
    paginate_by = 4


class PostDetail(DetailView):
    model = Post
    template_name = 'post.html'
    context_object_name = 'post'


class PostCreateView(PermissionRequiredMixin, LoginRequiredMixin, CreateView):
    permission_required = (
        'news.add_post',
    )
    template_name = 'post_create.html'
    form_class = PostForm


class PostUpdateView(PermissionRequiredMixin, LoginRequiredMixin, UpdateView):
    permission_required = (
        'news.change_post',
    )
    template_name = 'post_create.html'
    form_class = PostForm

    def get_object(self, **kwargs):
        id = self.kwargs.get('pk')
        return Post.objects.get(pk=id)


class PostDeleteView(PermissionRequiredMixin, DeleteView):
    permission_required = (
        'news.delete_post',
    )
    template_name = 'post_delete.html'
    queryset = Post.objects.all()
    success_url = '/news/'


class PostSearch(ListView):
    model = Post
    template_name = 'posts_search.html'
    context_object_name = 'posts_search'
    ordering = ['-id']

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = PostFilter(self.request.GET, queryset=self.get_queryset())
        return context


class Posts(View):
    def get(self, request):
        posts = Post.obejcts.order_by('-id')
        p = Paginator(posts, 1)
        posts = p.get_page(request.GET.get('page', 1))

        data = {
            'posts': posts,
        }

        return render(request, 'posts.html', data)


