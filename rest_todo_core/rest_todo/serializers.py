from django.contrib.auth import get_user_model
from rest_framework import serializers

from .forms import CustomUserCreationForm
from .models import UserPost


class UserPostSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = UserPost
        fields = ['user', 'id', 'post_title', 'post_body', 'user_id']


class CreateUserSerializer(serializers.ModelSerializer):
    # because there is no password2 field in the User model, i will exempt it from serialization
    password2 = serializers.CharField(style={"input_type": "password"}, write_only=True) 

    class Meta:
        model = get_user_model()
        fields = ['username', 'password', 'password2']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def save(self, **kwargs):
        password = self.validated_data.pop('password')
        # Seems like an ordered dict is a valid data kwarg,
        # so i won't unpack it into a native Python dict
        new_data = {'password1': password} | self.validated_data
        # i don't wanna use normal serializer and handle all the validation by myself
        # Maybe i should use this form for creating a user without a serializer at all? 
        # request.dict is already a native Python dict so i can pass it directly into the form like in vanilla Django.
        form = CustomUserCreationForm(data=new_data)
        if form.is_valid():
            self.instance = form.save()
            return self.instance

        raise serializers.ValidationError({'input_errors': form.errors}) # status is 400 by default
