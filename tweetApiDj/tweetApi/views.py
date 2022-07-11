from pickle import FALSE
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .tweeterapi.getApis import getRecentTweets
# Create your views here.
class TweetAppView(APIView):
    # 1. get recent tweet
    def get(self, request,id:str, *args, **kwargs):
        '''
        Get recent tweets
        '''
        tweet = getRecentTweets(id)
        print(tweet)
        # serializer = SeleniumSerializer(tweet, many=FALSE)
        
        return Response(tweet, status=status.HTTP_200_OK)

 