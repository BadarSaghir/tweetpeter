

from django.urls import path

from tweetApi.views import TodoListApiView


urlpatterns = [
    path("<str:id>/",TodoListApiView.as_view())

]