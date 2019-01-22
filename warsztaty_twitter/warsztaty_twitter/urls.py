from django.contrib import admin
from django.urls import path
from twitter_app import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.AllTweetsView.as_view(), name='main'),
    path('accounts/login/',views.LoginView.as_view(), name='login'),
    path('user/',views.CreateEditUserView.as_view(), name='user'),
    path('logout/',views.LogoutView.as_view(), name='logout'),
    path('user/change_password', views.ChangePasswordView.as_view(), name='change_user_password'),
    path('user/delete/<int:pk>', views.DeleteUserAccountView.as_view(), name='delete_user'),

    #Users
    path('userslist/', views.UsersView.as_view(), name='users_list'),

    path('tweet_detail/<int:pk>/', views.TweetDetailView.as_view(), name='tweet_detail'),
    path('tweets/<int:pk>/', views.UserTweetsView.as_view(), name='user_tweets'),
    path('tweet_update/<int:pk>/', views.TweetUpdateView.as_view(), name='tweet_update'),

    #messages
    path('messages/<int:pk>',views.UserMessagesView.as_view(), name='user_messages'),
    path('message_detail/<int:pk>', views.MessageDetailView.as_view(), name='message_detail'),
    path('message/delete/<int:pk>', views.DeleteMessageView.as_view(), name='delete_messsage'),

    #comment
    path('comment/delete/<int:pk>',views.DeleteCommentView.as_view(), name='delete_comment'),






]
