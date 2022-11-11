from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView

from rest_framework import generics, mixins, viewsets
from rest_framework import status, filters

from .models import Guest, Movie, Reservation
from .serializers import GuestSerializers, MovieSerializers, ReservationSerializers
# api/username


# no models no Rest API
def no_model_and_rest(request):
    data = [
        {
            'id': 1,
            'name': 'ahmed',
            'phone': 12456,
        },
        {
            'id': 2,
            'name': 'ali',
            'phone': 156466,
        },
        {
            'id': 3,
            'name': 'omar',
            'phone': 17989766,
        }
    ]
    return JsonResponse(data, safe=False)


# exist model no rest API
def model_no_rest(request):
    # guests = Guest.objects.all()
    guests = Guest.objects.filter(name__iexact='omar reda')

    # data = list(guests.values('user', 'name', 'mobile'))
    # return JsonResponse(data, safe=False)
    data = {
        "Guests": list(guests.values('user', 'name', 'mobile'))
    }
    return JsonResponse(data)


# Rest API -> GET, POST
@api_view(['GET'])
def rest_get(request):
    if request.method == 'GET':
        guest = Guest.objects.all()
        serializers = GuestSerializers(guest, many=True)
        return Response(serializers.data)


@api_view(['POST'])
def rest_post_method(request):
    if request.method == 'POST':
        serializers = GuestSerializers(data=request.data)
        if serializers.is_valid():
            # print(serializers)
            serializers.save()
            return redirect('/rest_get')


# Just one item
@api_view(['GET', 'PUT', 'DELETE'])
def rest_one_item(request, pk):
    guest = get_object_or_404(Guest, pk=pk)
    if request.method == 'GET':
        item_data = GuestSerializers(guest)
        return Response(item_data.data)

    elif request.method == 'PUT':
        item_data = GuestSerializers(guest, request.data)
        if item_data.is_valid():
            item_data.save()
            # return redirect(f'/rest_one/{guest.pk}/')
            # return redirect(guest.get_put_url())
            return Response(request.data)
    elif request.method == 'DELETE':
        # item_data = GuestSerializers(guest, request.data)
        guest.delete()
        # error here
        return redirect(guest.get_put_url())


# CBV -> GET and POST
class RestCBV(APIView):
    def get(self, request):
        guest = Guest.objects.all()
        serializers = GuestSerializers(guest, many=True)
        return Response(serializers.data)

    def post(self):
        serializers = GuestSerializers(data=request.data)
        if serializers.is_valid():
            # print(serializers)
            serializers.save()
            return redirect('/rest_get')


# 4.2 GET PUT DELETE cloass based views -- pk
class CBV_pk(APIView):

    def get_object(self, pk):
        try:
            return Guest.objects.get(pk=pk)
        except Guest.DoesNotExists:
            raise Http404

    def get(self, request, pk):
        guest = self.get_object(pk)
        serializer = GuestSerializers(guest)
        return Response(serializer.data)

    def put(self, request, pk):
        guest = self.get_object(pk)
        serializer = GuestSerializers(guest, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        guest = self.get_object(pk)
        guest.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

# 5 Mixins
# 5.1 mixins list


class mixins_list(mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView):
    queryset = Guest.objects.all()
    serializer_class = GuestSerializers

    def get(self, request):
        return self.list(request)

    def post(self, request):
        return self.create(request)

# 5.2 mixins get put delete


class mixins_pk(mixins.RetrieveModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin, generics.GenericAPIView):
    queryset = Guest.objects.all()
    serializer_class = GuestSerializers

    def get(self, request, pk):
        return self.retrieve(request)

    def put(self, request, pk):
        return self.update(request)

    def delete(self, request, pk):
        return self.destroy(request)

# 6 Generics
# 6.1 get and post


class generics_list(generics.ListCreateAPIView):
    queryset = Guest.objects.all()
    serializer_class = GuestSerializers
    # authentication_classes = [TokenAuthentication]
    # permission_classes = [IsAuthenticated]

# 6.2 get put and delete


class generics_pk(generics.RetrieveUpdateDestroyAPIView):
    queryset = Guest.objects.all()
    serializer_class = GuestSerializers
    # authentication_classes = [TokenAuthentication]
    # permission_classes = [IsAuthenticated]


# 7 viewsets
class viewsets_guest(viewsets.ModelViewSet):
    queryset = Guest.objects.all()
    serializer_class = GuestSerializers


class viewsets_movie(viewsets.ModelViewSet):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializers
    filter_backend = [filters.SearchFilter]
    search_fields = ['movie']


class viewsets_reservation(viewsets.ModelViewSet):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializers
