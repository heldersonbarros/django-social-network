from rest_framework import serializers
from .models import Post, Comment
from accounts.serializers import UserSerializer
from communities.serializers import CommunitySerializer

class PostSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    community = CommunitySerializer(read_only=True)
    like_count = serializers.IntegerField(source='like_set.count', read_only=True)
    liked = serializers.SerializerMethodField()
    owner = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = '__all__'

    def get_liked(self, obj):
        #user =  self.context['request'].user mais fácil
        if self.context['user'] != None:
            return obj.like_set.filter(user=self.context['user']).exists()
        return False

    def get_owner(self, obj):
        return self.context['user'].id == obj.user.id

class CommentSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    
    class Meta:
        model = Comment
        fields = '__all__'