import django.forms as forms
from django.contrib.auth.forms import UserCreationForm
from .models import Tweet, Comment, Message, User   #abstract user!


class LoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput(), max_length=70)


class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']



class TweetForm(forms.ModelForm):
    class Meta:
        model = Tweet
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={'rows': '5', 'cols': '40'}),
        }


class EditUser(forms.ModelForm):
    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name', 'info', 'location']


class ChangePassword(forms.Form):
    new_password = forms.CharField(widget=forms.PasswordInput(), max_length=70)
    repeat_password = forms.CharField(widget=forms.PasswordInput(), max_length=70)


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 5, 'cols': 40}),
        }


class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 5, 'cols': 40}),
        }

