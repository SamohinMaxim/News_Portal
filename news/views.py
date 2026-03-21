from django.contrib.auth.mixins import PermissionRequiredMixin
from django.core.mail import send_mail
from django.urls import reverse_lazy
from django.utils import timezone
import datetime
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.shortcuts import redirect, render, get_object_or_404
from django_filters.views import FilterView
from sqlparse.engine.grouping import group

from .forms import PostForm
from .models import Post, Author, Category, PostCategory
from .filters import PostFilter
from .utils import create_or_edit
from django.contrib.flatpages.models import FlatPage

from sign.utils import request_object


class PostListView(FilterView):
    model = Post
    context_object_name = 'posts'
    template_name = 'news/post_list.html'
    ordering = ('-created_ad',)
    paginate_by = 10
    filterset_class = PostFilter

class NewsSearchView(ListView):
    model = Post
    template_name = 'news/search.html'
    context_object_name = 'news_list'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        query = self.request.GET.get('q', '')
        author_name = self.request.GET.get('author', '')
        date_from = self.request.GET.get('date_from', '')

        if query:
            queryset = queryset.filter(title__icontains=query)

        if author_name:
            queryset = queryset.filter(author__user__username__icontains=author_name)

        if date_from:
            try:
                date_from = datetime.datetime.strptime(date_from, '%Y-%m-%d').date()
                queryset = queryset.filter(created_ad__gte=date_from)
            except ValueError:
                pass

        return queryset.order_by('-created_ad')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['query'] = self.request.GET.get('q', '')
        context['author_name'] = self.request.GET.get('author', '')
        context['date_from'] = self.request.GET.get('date_from', '')
        return context

def news_list(request):
    posts = Post.objects.all().order_by('-dataCreations')
    return render(request, 'news/list.html', {'posts': posts})



class PostDetailView(DetailView):
    model = Post
    context_object_name = 'post'
    template_name = 'news/post_detail.html'

def post_detail(request, pk):
    post = Post.objects.get(pk=pk)
    return render(request, 'news/post_detail.html', {'posts': post})


class PostCreateView(PermissionRequiredMixin,CreateView):
    model = Post
    form_class = PostForm
    template_name = 'news/post_create_or_update.html'
    permission_required = 'news.add_post'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        path_create = reverse_lazy('news_create')
        return create_or_edit(context, self.request.path)

    def form_valid(self, form):
        response = super().form_valid(form)
        group_subscribers = request_object('subscribers')
        subscribers_users = group_subscribers.user_set.values_list('email', flat=True)
        send_mail(
            subject='Уведомление по подписке!',
            message='Появилась новая публикация на Новостном портале',
            from_email='server@server.ru',
            recipient_list=subscribers_users,
        )
        return response

class PostUpdateView(UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'news/post_create_or_update.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return create_or_edit(context, self.request.path)

class PostDeleteView(DeleteView):
    model = Post
    context_object_name = 'post'
    template_name = 'news/delete.html'
    success_url = reverse_lazy('post_list')


class BasePostViewMixin:
    model = Post
    form_class = PostForm
    template_name = 'news/post_form.html'

    def form_valid(self, form):
        post = form.save(commit=False)
        if 'news' in self.request.path:
            post.post_type = 'новость'
        elif 'articles' in self.request.path:
            post.post_type = 'статья'
        return super().form_valid(form)


class NewsCreateView(BasePostViewMixin, CreateView):
    success_url = reverse_lazy('news_list')


class NewsUpdateView(BasePostViewMixin, UpdateView):
    success_url = reverse_lazy('news_list')


class NewsDeleteView(BasePostViewMixin, DeleteView):
    success_url = reverse_lazy('news_list')


class ArticleCreateView(BasePostViewMixin, CreateView):
    success_url = reverse_lazy('news_list')


class ArticleUpdateView(BasePostViewMixin, UpdateView):
    success_url = reverse_lazy('news_list')


class ArticleDeleteView(BasePostViewMixin, DeleteView):
    success_url = reverse_lazy('news_list')




# def post_add(request):
#     if request.method == 'POST':
#         kwargs = {
#             'author_id': request.POST.get('author'),
#             'title': request.POST.get('title'),
#             'text': request.POST.get('text'),
#         }
#         category_ids = request.POST.getlist('categories')
#         post = Post.objects.create(**kwargs)
#         for category_id in category_ids:
#             PostCategory.objects.create(post=post, category_id=category_id)
#         return redirect('post_detail', pk=post.pk)
#     authors = Author.objects.all()
#     categories = Category.objects.all()
#     return render(request, 'news/post_add.html', {'authors': authors, 'categories': categories})
#
#  def post_edit(request, pk):
#      post = get_object_or_404(Post, pk=pk)
#
#      if request.method == 'POST':
#          post.author_id = request.POST.get('author')
#          post.title = request.POST.get('title')
#          post.text = request.POST.get('text')
#          post.save()
#
#          categories = request.POST.getlist('categories')
#          post.category.set(categories)
#
#          return redirect('post_detail', pk=post.pk)
#
#      authors = Author.objects.all()
#      categories = Category.objects.all()
#      selected_categories = post.category.values_list('id', flat=True)
#
#      return render(request, 'news/post_edit.html', {
#          'post': post,
#          'authors': authors,
#          'categories': categories,
#          'selected_categories': selected_categories,
#      })