import re
from datetime import date
from dateutil.relativedelta import relativedelta
from django.contrib.auth import get_user_model

from rest_framework import serializers

from . import models


def base_validator(to_validate, list_to_check):
    acceptable_characters = [x[0] for x in list_to_check]
    letters = re.findall(r'\w', to_validate)
    for letter in letters:
        if letter not in acceptable_characters:
            raise serializers.ValidationError(
                "You can only send {}".format(
                    ", ".join(acceptable_characters)
                )
            )
    return ",".join(letters)


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    def create(self, validated_data):
        user = get_user_model().objects.create(
            username=validated_data['username'],
        )
        user.set_password(validated_data['password'])
        user.save()
        return user

    class Meta:
        model = get_user_model()


class DogSerializer(serializers.ModelSerializer):

    born = serializers.SerializerMethodField()
    status = serializers.SerializerMethodField()

    class Meta:
        model = models.Dog
        fields = (
            'id',
            'name',
            'image_path',
            'breed',
            'age',
            'gender',
            'size',
            'born',
            'status',
        )

    def get_born(self, obj):
        months = obj.age
        birthday_dt = date.today() - relativedelta(months=months)
        birthday_str = birthday_dt.strftime('%B %Y')
        return birthday_str

    def get_status(self, obj):
        return "Status to appear here"


class UserPrefSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.UserPref
        fields = (
            'age',
            'gender',
            'size',
        )
        extra_kwargs = {
            'user': {
                'write_only': True
            }
        }

    def validate_age(self, value):
        base_validator(value, models.AGE_CHOICES)

    def validate_gender(self, value):
        base_validator(value, models.GENDER_CHOICES)

    def validate_size(self, value):
        base_validator(value, models.SIZE_CHOICES)


class UserDogSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.UserDog
        fields = (
            'dog',
            'status',
        )
        extra_kwargs = {
            'user': {
                'write_only': True
            }
        }
