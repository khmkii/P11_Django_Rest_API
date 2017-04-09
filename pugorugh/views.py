from django.contrib.auth import get_user_model
from django.core.urlresolvers import reverse_lazy
from django.db.models import Q
from django.http import Http404
from django.shortcuts import get_object_or_404
from rest_framework import permissions
from rest_framework import status
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from . import models
from . import serializers


acceptable_filter_strings = [option[1].lower() for option in models.STATUS_CHOICES]


def check_filter_string(filter_string):
    if filter_string in acceptable_filter_strings:
        return True
    else:
        return False


class UserRegisterView(CreateAPIView):
    permission_classes = (permissions.AllowAny,)
    model = get_user_model()
    serializer_class = serializers.UserSerializer


class DogListView(APIView):

    def get(self, request, filter='', format=None):
        if filter:
            if check_filter_string(filter):
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
            elif filter == 'match':
                pass
                # TODO complete this to match all dogs with user preferences
            else:
                url = reverse_lazy('pugorugh:all_dogs')
                good_paths = [url + word for word in acceptable_filter_strings] + ['match']
                response_text = "Bad filter, try one of these: " + ", ".join(good_paths)
                return Response(response_text, status=status.HTTP_400_BAD_REQUEST)
        else:
            dogs = models.Dog.objects.all()
            serializer = serializers.DogSerializer(dogs, many=True)
            return Response(serializer.data)

    def post(self, request, filter='', format=True):
        if filter:
            return Response("Not allowed with URL parameter after 'dogs/'", status=status.HTTP_405_METHOD_NOT_ALLOWED)
        else:
            serializer = serializers.DogSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DogDetailView(APIView):
    
    def get_dog_object(self, pk):
        return get_object_or_404(models.Dog, pk=pk)

    def get(self, request, pk, format=None):
        dog = self.get_dog_object(pk)
        serializer = serializers.DogSerializer(dog)
        return Response(serializer.data)


class RatedDog(APIView):

    def get_user_dog_object(self, request, pk):
        try:
            dog = models.Dog.objects.get(pk=pk)
        except models.Dog.DoesNotExist:
            raise Http404
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
        if check_filter_string(rating):
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
            raise Http404


class NextDog(APIView):

    def get_next_dog(self, pk, rating, user):
        dog = models.Dog.objects.get(pk=pk)
        user_filtered_dogs_pk = [
            user_dog.dog.pk for user_dog in models.UserDog.objects.filter(
                Q(user=user) & Q(status__exact=rating[0])).all()
            ]
        if user_filtered_dogs_pk[-1] == pk:
            return None
        else:
            current_dog_ix = user_filtered_dogs_pk.index(int(pk))
            next_dog_ix = current_dog_ix + 1
            next_dog_pk = user_filtered_dogs_pk[next_dog_ix]
            return next_dog_pk

    def get(self, request, pk, rating):
        if check_filter_string(rating):
            user = request.user
            pk_for_next_dog = self.get_next_dog(pk, rating, user)
            if pk_for_next_dog is not None:
                return_dog = models.Dog.objects.get(pk=pk_for_next_dog)
                serializer = serializers.DogSerializer(instance=return_dog)
                next = reverse_lazy(
                    'pugorugh:next_dog',
                    kwargs={
                        'pk': pk_for_next_dog,
                        'rating': rating
                    })
                data = serializer.data
                data.update(
                    {'next': next}
                )
                return Response(data, status=status.HTTP_200_OK)
            else:
                pass
                # case for no next dog
        else:
            raise Http404


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
