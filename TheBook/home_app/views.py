from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views import View
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


from django.views.generic import CreateView, UpdateView, DeleteView

from home_app.models import Post, Comment
from login_app.models import CustomUser


class IndexView(View):
    def get(self, request):
        if not request.user.is_authenticated:
            return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
        users = CustomUser.objects.all()
        return render(request, 'home_app/base.html', context={'users': users})


class HomeView(View):
    def get(self, request):
        if not request.user.is_authenticated:
            return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
        id = request.user.id
        user = CustomUser.objects.get(id=id)
        followed_users = []
        followed_users.append(user) #loggedin user is being followed
        for r in user.initiated_relations.all():
            followed_users.append(r.receiver)
        posts = Post.objects.filter(author__in=followed_users)
        #Add pagination:
        paginator = Paginator(posts, 5)
        page = request.GET.get('page')
        try:
            posts = paginator.page(page)
        except PageNotAnInteger:
            posts = paginator.page(1)
        except EmptyPage:
            posts = paginator.page(paginator.num_pages)
        users = CustomUser.objects.all()
        return render(request, 'home_app/posts.html', context={'posts': posts, 'users': users, page: 'page'})


class PostCreateView(CreateView):
    model = Post
    fields = ['title', 'body', 'status']
    # template_name = 'home_app/post_form.html' #name is default
    success_url = reverse_lazy('home-view')

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return super().get(request, *args, **kwargs)
        else:
            return redirect('login-view')


class PostUpdateView(UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'body', 'status']
    template_name = 'home_app/post_update.html'  # name is NOT default(default is post_detail)
    success_url = reverse_lazy('home-view')

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


class PostDeleteView(UserPassesTestMixin, DeleteView):
    model = Post
    success_url = reverse_lazy('home-view')

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


# def PostLike(request, pk):
#     post = Post.objects.ged(id=pk)
#     post.likes.add(request.user)
#     return HttpResponseRedirect(reverse('home-view'))


# class PostLike(View):
#     def post(self, request, pk):
#         post = Post.objects.get(id=self.kwargs['pk'])
#         post.likes.add(request.user)

        # print(CustomUser.objects.get(id=request.user.id).liked_posts.all())

#         return redirect('home-view')


class PostLike(View):
    def post(self, request, pk):
        post = Post.objects.get(id=pk)
        post.likes.add(request.user)
        return redirect('home-view')


class AddComment(LoginRequiredMixin, CreateView):
    model = Comment
    fields = ['body']
    # template_name = 'home_app/comment_form.html' #name is default
    success_url = reverse_lazy('home-view')

    def form_valid(self, form):
        form.instance.author = self.request.user
        path = self.request.path
        post_id = int(path.split('/')[2])
        form.instance.post = Post.objects.get(id=post_id)
        return super().form_valid(form)
