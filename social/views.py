import datetime

from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Post, Like, Logger
from rest_framework import serializers
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from django.contrib.auth.models import User


class Log_seriz(serializers.ModelSerializer):
    data = serializers.DateField(source='oDate')
    action = serializers.CharField(source='aAction')
    class Meta:
        model = Logger
        fields = ['data', 'action']


class User_seriz(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username']


class Post_seriz_list(serializers.ModelSerializer):
    user = User_seriz(source='nUser_id')
    post_text = serializers.CharField(source='aPost_text')
    postid = serializers.IntegerField(source='id')
    class Meta:
        model = Post
        fields = ['postid', 'post_text', 'user']
        depth = 1
    def to_representation(self, instance):
        oLike_objects = Like.objects.filter(nPost_id=instance.id, aAction='like')
        oUnlike_objects = Like.objects.filter(nPost_id=instance.id, aAction='unlike')

        oLikes_json = Like_seriz_to_post(oLike_objects, many=True)
        oUnlikes_json = Like_seriz_to_post(oUnlike_objects, many=True)

        oPost_json = {
            'postid': instance.id,
            'post_owner': instance.nUser_id.username,
            'post': instance.aPost_text,
            'likes': oLikes_json.data,
            'unlikes': oUnlikes_json.data
        }
        return oPost_json


class Like_seriz_to_post(serializers.ModelSerializer):
    class Meta:
        model = Like
    def to_representation(self, instance):
        oReturn_json = {
            'from_who': instance.nUser_id.username,
            'date': instance.oDate
        }
        return oReturn_json


class Like_seriz(serializers.ModelSerializer):
    likeunlike = serializers.CharField(source='aAction')
    data = serializers.DateField(source='oDate')
    user = User_seriz(source='nUser_id')
    class Meta:
        model = Like
        fields = ['nPost_id', 'likeunlike', 'data', 'user']
        depth = 1
    def to_representation(self, instance):
        oLike_json = {
            'postid':instance.nPost_id.id,
            'post': instance.nPost_id.aPost_text,
            'like/unlike': instance.aAction,
            'post_owner': instance.nPost_id.nUser_id.username,
            'like_from': instance.nUser_id.username
        }
        return oLike_json
    def to_internal_value(self, data):
        oPost_object = Post.objects.filter(pk=data.get('nPost_id')).first()
        oData = {
            'nUser_id'      : data.get('user'),
            'nPost_id'  : oPost_object,
            'aAction': data.get('likeunlike'),
            'oDate'      : data.get('data')
        }
        return oData

    def create(self, validated_data):
        return Like.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.oDate = validated_data.get('data')
        instance.aAction = validated_data.get('likeunlike')
        instance.save(force_update=True)
        return instance


# Create your views here.
class Post_view(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
    aClass = 'view'
    def get(self, request):
        oPost = Post.objects.all()
        oPost_seriz = Post_seriz_list(oPost, many=True)
        return Response(oPost_seriz.data)

    def post(self, request):
        oPost_save = Post(
            nUser_id=self.request.user,
            aPost_text=self.request.data['post']
        )
        oPost_save.save()
        return Response({'detail':200})


class Like_view(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
    def get(self, request):
        oLike = Like.objects.all()
        oLike_seriz = Like_seriz(oLike, many=True)
        return Response(oLike_seriz.data)

    def post(self, request):
        oNow = datetime.datetime.now().date()
        nPost_id = self.request.data['postid']
        aAction = self.request.data['action']
        oData = {
            'user': self.request.user,
            'nPost_id': nPost_id,
            'likeunlike': aAction,
            'data': datetime.datetime.now().date()
        }
        oLike_post_seriz = Like_seriz(data=oData)
        if oLike_post_seriz.is_valid():
            oInstance = Like.objects.filter(nPost_id=nPost_id, nUser_id=self.request.user)
            if oInstance.count() > 0:
                oLike_post_seriz.update(oInstance.first(), oData)
            else:
                oLike_post_seriz.save()
        if oLike_post_seriz != {}:
            return Response(oLike_post_seriz.errors)
        return Response({'detail':'200'})


class Analitic_view(APIView):
    def get(self, request):
        aDate_from = self.request.query_params.get('date_from')
        aDate_to = self.request.query_params.get('date_to')
        try:
            nNumber_likes = Like.objects.filter(oDate__range=(aDate_from, aDate_to)).count()
        except  Exception as oErr:
            return Response({'error': oErr})
        return Response({'count_likes': nNumber_likes})


class User_view(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        q = Logger.objects.filter(nUser_id=self.request.user.pk)
        oUsers = Log_seriz(q, many=True)
        return Response(oUsers.data)







