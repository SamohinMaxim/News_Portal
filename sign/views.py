from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.models import User, Group
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.contrib import messages

from news.forms import PostForm
from news.models import Author, Post
from .utils import request_object

from .forms import SignUpForm


class SignUpForm(CreateView):
    model = User
    template_name = 'sign/signup.html'
    form_class = SignUpForm
    success_url = reverse_lazy('user_profile')


def confirm_logout(request):
    return render(request, 'sign/confirm_logout.html')

@login_required
def user_profile(request):
    context = {
        'is_author': request.user.groups.filter(name='authors_').exists(),
    }
    return render(request, 'sign/profile.html', context)



@login_required
def be_author(request):
    request_object(Author, user=request.user)
    group_authors_ = request_object(Group, name='authors_')

    if not request.user.groups.filter(name='authors_').exists():
        request.user.groups.add(group_authors_)

    list(messages.get_messages(request))
    messages.success(request,
                     'Вы успешно стали автором!',
                     extra_tags='authors_'
                     )

    return redirect(request.META.get('HTTP_REFERER'))


@permission_required('app_name.edit_post')
def edit_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            return redirect('post_detail', post_id=post.id)
    else:
        form = PostForm(instance=post)
    return render(request, 'edit_post.html', {'form': form})

