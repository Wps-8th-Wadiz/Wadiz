from django.urls import path

from .. import apis

urlpatterns = [
    path('', apis.UserList.as_view()),
    path('list-create/', apis.UserList.as_view()),
    path('login-auth-token/', apis.AuthToken.as_view()),
    path('detail/<int:pk>/', apis.UserDetail.as_view()),
]
