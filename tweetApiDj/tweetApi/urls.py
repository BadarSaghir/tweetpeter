

from django.urls import path

from tweetApi.views import TweetAppView


urlpatterns = [
    path("<str:id>/",TweetAppView.as_view())

]