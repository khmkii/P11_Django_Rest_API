from django.contrib.auth import get_user_model
from django.core.urlresolvers import reverse_lazy
from django.http import Http404
from django.db.models import Q
from rest_framework import permissions
from rest_framework import status
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from . import models
from . import serializers


class UserRegisterView(CreateAPIView):
    permission_classes = (permissions.AllowAny,)
    model = get_user_model()
    serializer_class = serializers.UserSerializer


class DogListView(APIView):

    def get(self, request, filter='', format=None):
        if filter:
            filter_keywords = [option[1].lower() for option in models.STATUS_CHOICES]
            if filter in filter_keywords:
                filter_on = [
                    filter_word[0] for filter_word in
                    models.STATUS_CHOICES if filter_word[1].lower() == filter
                    ].pop()
                user_dogs = models.UserDog.objects.filter(
                    Q(user=request.user) & Q(status__exact=filter_on)
                ).all().select_related('dog')
                dogs = [users_dog.dog for users_dog in user_dogs]
                serializer = serializers.DogSerializer(dogs, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                url = reverse_lazy('pugorugh:all_dogs')
                good_paths = [url + word for word in filter_keywords]
                response_text = "Bad filter, try one of these: " + ", ".join(good_paths)
                return Response(response_text, status=status.HTTP_400_BAD_REQUEST)
        else:
            dogs = models.Dog.objects.all()
            serializer = serializers.DogSerializer(dogs, many=True)
            return Response(serializer.data)

    def post(self, request, filter='',format=True):
        if filter:
            return Response("Cannot POST here", status=status.HTTP_400_BAD_REQUEST)
        else:
            serializer = serializers.DogSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DogDetailView(APIView):
    
    def get_dog_object(self, pk):
        try:
           return models.Dog.objects.get(pk=pk)
        except models.Dog.DoesNotExist:
            return Http404

    def get(self, request, pk, format=None):
        dog = self.get_dog_object(pk)
        serializer = serializers.DogSerializer(dog)
        return Response(serializer.data)


class RatedDog(APIView):

    def get_user_dog_object(self, request, pk):
        try:
            dog = models.Dog.objects.get(pk=pk)
        except models.Dog.DoesNotExist:
            return Http404
        else:
            try:
                return models.UserDog.objects.get(dog=dog)
            except models.UserDog.DoesNotExist:
                new_user_dog = models.UserDog.objects.create(
                    dog=dog,
                    user=request.user
                )
                return new_user_dog

    def post(self, request, pk, rating, format=None):
        if rating in [option[1].lower() for option in models.STATUS_CHOICES]:
            user_dog = self.get_user_dog_object(request, pk)
            user_dog.status = [
                preference[0] for preference in
                models.STATUS_CHOICES if
                preference[1].lower() == rating
                ].pop(0)
            user_dog.save()
            serializer = serializers.UserDogSerializer(instance=user_dog)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Http404


class NextDog(APIView):
    pass


class SeeUpdatePreferencesView(APIView):

    def get(self, request, format=None):
        try:
            user_pref = models.UserPref.objects.get(user=request.user)
        except models.UserPref.DoesNotExist:
            user_pref = models.UserPref.objects.create(user=request.user)

        serializer = serializers.UserPrefSerializer(user_pref)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, format=None):
        user_pref = models.UserPref.objects.get(user=request.user)
        serializer = serializers.UserPrefSerializer(user_pref, data=request.data)
        import pdb
        pdb.set_trace()
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
