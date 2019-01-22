from django.shortcuts import render, redirect, get_object_or_404, reverse
from django.views import View
from .forms import LoginForm, CreateUserForm, TweetForm, EditUser, CommentForm, MessageForm
from .models import *
from django.contrib.auth import authenticate, login, logout
from django.views.generic.detail import DetailView
from django.views.generic import ListView
from django.views.generic.edit import DeleteView
from django.db.models import Q
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic.edit import UpdateView
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.http import Http404



class LoginView(View):
    def get(self, request):
        form = LoginForm()
        ctx = {'form': form}
        return render(request, 'twitter_app/login.html', ctx)

    def post(self, request):
        form = LoginForm(request.POST)
        x = None
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            if User.objects.filter(email=email):  # email unikalny!
                u = User.objects.filter(email=email)[0].username
                login_user = authenticate(username=u, password=password)
                if login_user is not None:
                    login(request, login_user)
                    return redirect('main')

        x = 'Unknown user! Try again.'
        ctx = {'form': form, 'x': x}
        return render(request, 'twitter_app/login.html', ctx)


class LogoutView(LoginRequiredMixin, View):
    def get(self, request):
        logout(request)
        return redirect('/')


class CreateEditUserView(View):
    def get(self, request):
        if request.user.is_authenticated:
            form = EditUser(instance=request.user)
            t = 'Edit User'
        else:
            t = 'Create New User'
            form = CreateUserForm()
        ctx = {'form': form, 't': t}
        return render(request, 'twitter_app/create_edit_user.html', ctx)

    def post(self, request):
        if request.user.is_authenticated:
            form = EditUser(request.POST, instance=request.user)
            t = 'Edit User'
        else:
            t = 'Create New User'
            form = CreateUserForm(request.POST)
        ctx = {'form': form}
        if form.is_valid():
            form.save()
            if 'New' in t:
                # logowanie
                raw_password = form.cleaned_data.get('password1')
                user = authenticate(username=form.instance.username, password=raw_password)
                login(request, user)
            return redirect('main')

        return render(request, 'twitter_app/create_edit_user.html', ctx)


class ChangePasswordView(LoginRequiredMixin, View):
    def get(self, request):
        form = PasswordChangeForm(request.user)
        ctx = {'form': form}
        return render(request, 'twitter_app/change_password.html', ctx)

    def post(self, request):
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
            return redirect('user')
        else:
            ctx = {'form': form}
            return render(request, 'twitter_app/change_password.html', ctx)


class DeleteUserAccountView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = User
    success_url = '/'

    def test_func(self):
        return self.request.user == self.get_object()



class AllTweetsView(LoginRequiredMixin, ListView):
    model = Tweet
    queryset = Tweet.objects.filter(disabled=False)
    ordering = '-creation_date'
    template_name = 'twitter_app/base.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = TweetForm()
        return context

    def post(self, request, *args, **kwargs):
        form = TweetForm(request.POST)
        if form.is_valid():
            form.instance.user = request.user
            form.save()
            return redirect(form.instance)


class TweetDetailView(LoginRequiredMixin, DetailView):
    model = Tweet

    def get_object(self, queryset=None):
        obj = super().get_object()
        if not obj.disabled:
            return obj
        else:
            raise Http404

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = CommentForm()
        context['comments'] = self.get_object().comment_set.filter(disabled=False)
        return context

    def post(self, request, *args, **kwargs):
        form = CommentForm(request.POST)
        if form.is_valid():
            form.instance.user = request.user
            form.instance.tweet = self.get_object()
            form.save()
            return redirect(self.get_object())



class TweetUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Tweet
    form_class = TweetForm
    template_name_suffix = '_update_form'

    def test_func(self):
        return self.request.user == self.get_object().user

    def get_object(self, queryset=None):
        obj = super().get_object()
        if not obj.disabled:
            return obj
        else:
            raise Http404


class UserTweetsView(LoginRequiredMixin, ListView):
    template_name = 'twitter_app/user_tweets.html'

    def get_queryset(self):
        self.user = get_object_or_404(User, pk=self.kwargs.get('pk'))
        ts = Tweet.objects.filter(user=self.user, disabled=False)
        if ts:
            return ts
        else:
            x = Tweet()
            x.user = self.user
            return [x, 'empty']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = self.user
        context['form'] = MessageForm()
        return context

    def post(self, request, *args, **kwargs):
        form = MessageForm(request.POST)
        if form.is_valid():
            if request.user != self.get_queryset()[0].user:  # nie mozna wysylac wiadomosci do samego siebie
                form.instance.sender = request.user
                form.instance.receiver = self.get_queryset()[0].user
                form.save()
                messages.success(request, 'Message was successfully sent!')
                return redirect(reverse('user_tweets', kwargs={'pk': self.get_queryset()[0].user.id}))


class UserMessagesView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    template_name = 'twitter_app/user_messages.html'

    def test_func(self):
        if User.objects.filter(pk=self.kwargs.get('pk')):
            return self.request.user == User.objects.filter(pk=self.kwargs.get('pk'))[0]
        else:
            raise Http404

    def get_queryset(self):
        self.user = get_object_or_404(User, pk=self.kwargs.get('pk'))
        return Message.objects.filter(disabled=False).filter(Q(sender=self.user) | Q(receiver=self.user)).order_by('-creation_date')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = self.user
        return context


class MessageDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = Message

    def test_func(self):
        return self.request.user in (self.get_object().sender, self.get_object().receiver)

    def get_object(self, queryset=None):
        obj = super().get_object()
        if not obj.disabled:
            return obj
        else:
            raise Http404


class DeleteMessageView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Message

    def get_success_url(self):
        return reverse('user_messages', kwargs={'pk': self.get_object().receiver.pk})


    def test_func(self):
        return self.request.user == self.get_object().receiver

    def get_object(self, queryset=None):
        obj = super().get_object()
        if not obj.disabled:
            return obj
        else:
            raise Http404


class DeleteCommentView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Comment

    def get_success_url(self):
        return reverse('tweet_detail', kwargs={'pk': self.get_object().tweet.pk} )

    def test_func(self):
        return self.request.user == self.get_object().user

    def get_object(self, queryset=None):
        obj = super().get_object()
        if not obj.disabled:
            return obj
        else:
            raise Http404


class UsersView(LoginRequiredMixin, ListView):
    model = User

