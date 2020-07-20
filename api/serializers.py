from django.contrib.auth import get_user_model
from rest_framework.serializers import ModelSerializer, ListField, CharField, PrimaryKeyRelatedField
from api.models import *


User = get_user_model()

class UserModelSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id',
            'first_name',
            'last_name',
            'username',
            'email',
            'password',
        ]
        extra_kwargs = {
            'password' : {
                'write_only' : True,
                'style' : {
                    'input_type' : 'password',
                    }
                },
            }

    def create(self, validated_data):
        user = User.objects.create_user(
            first_name = validated_data['first_name'],
            last_name = validated_data['last_name'],
            username = validated_data['username'],
            email = validated_data['email'],
            password = validated_data['password']
        )
        return user

    def update(self, instance, validated_data):
        """Handle updating user account"""
        if 'password' in validated_data:
            password = validated_data.pop('password')
            instance.set_password(password)

        return super().update(instance, validated_data)


class MovieSerializer(ModelSerializer):
    cast = ListField(
        child = CharField(required = False), required = False,
        min_length = 0
    )
    genre = ListField(
        child = CharField(required = False), required = False,
        min_length = 0
    )

    directors = ListField(
            child = CharField(required = False), required = False,
            min_length = 0
        )

    class Meta:
        model = Movie
        fields = '__all__'
        extra_kwargs = {
            'avg_rating' : {
                'read_only' : True,

                },
            'num_ratings' :{
                'read_only' : True,
            },
            }


class ReviewSerializer(ModelSerializer):
    reviewer = PrimaryKeyRelatedField(read_only = True)
    class Meta:
        model = Review
        fields = '__all__'
