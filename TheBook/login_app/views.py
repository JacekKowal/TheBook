from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.db.models import Q
from django.shortcuts import render, HttpResponse, redirect
from django.views import View

from home_app.models import Post
from .models import CustomUser, Relations, Messages


class LoginView(View):
    def get(self, request):
        return render(request, 'login_app/login_page.html')

    def post(self, request):
        username = request.POST['name']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            url = request.GET.get('next', '/')
            login(request, user)
            return redirect(url)
        else:
            return render(request, 'login_app/login_page.html')


class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('login-view')


class CreateUserView(View):
    def get(self, request):
        return render(request, 'login_app/register_page.html')

    def post(self, request):
        username = request.POST['name']
        password = request.POST['password']
        password2 = request.POST['password2']
        email = request.POST['email']
        if password == password2:
            try:
                CustomUser.objects.create_user(username, email, password2)
            except IntegrityError:
                return HttpResponse("<h1>Nazwa użytkownika już istnieje! :(<h1>")
            return redirect('home-view')
        else:
            return render(request, 'login_app/register_page.html')


class ProfileView(View):
    def get(self, request, pk):
        if request.user.is_authenticated:
            followed_users = []
            user = CustomUser.objects.get(id=pk)
            followed_users.append(user)
            posts = Post.objects.filter(author__in=followed_users)
            if request.user.id == pk:
                return render(request, 'login_app/profile_page.html', {'posts': posts})
            else:
                other_user = CustomUser.objects.get(id=pk)
                try:
                    other_user.received_relations.get(initiator=request.user)
                    ctx = {'other_user': other_user, 'followed': True, 'posts': posts}
                except Relations.DoesNotExist:
                    ctx = {'other_user': other_user, 'followed': False, 'posts': posts}
                return render(request, 'login_app/other_user_page.html', ctx)
        else:
            return redirect('login-view')

    def post(self, request, pk):
        user = request.user
        user.username = request.POST['name']
        user.email = request.POST['email']
        if request.POST['profile_pic']:
            user.image = "profile_pics/" + request.POST['profile_pic']
        user.save()
        return redirect('profile-view', user.id)


class FollowView(View):
    def post(self, request, pk):
        initiator = request.user
        receiver = CustomUser.objects.get(id=pk)
        Relations.objects.create(initiator=initiator, receiver=receiver)
        return redirect('profile-view', pk)


class UnfollowView(View):
    def post(self, request, pk):
        initiator = request.user
        receiver = CustomUser.objects.get(id=pk)
        Relations.objects.filter(initiator=initiator, receiver=receiver).delete()
        return redirect('profile-view', pk)


class SendMessageView(View):
    def get(self, request, pk):
        to_user = CustomUser.objects.get(id=pk)
        return render(request, 'login_app/send_message.html', {'to_user': to_user})

    def post(self, request, pk):
        author = request.user
        body = request.POST['body']
        # receiver = CustomUser.objects.get(username=f"{request.POST['to_user']}")
        receiver = CustomUser.objects.get(id=pk)
        Messages.objects.create(receiver=receiver, author=author, body=body)
        return redirect('profile-view', receiver.id)


class MessagesView(View):
    def get(self, request):
        followed = []
        user = request.user
        for relation in Relations.objects.filter(initiator=user):
            followed.append(relation.receiver)
        messages_from = Messages.objects.filter(receiver=user)
        messages_to = Messages.objects.filter(author=user)
        return render(request, 'login_app/messages.html', {'followed': followed, 'messages_from': messages_from, 'messages_to': messages_to})

