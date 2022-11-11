from django.urls import path, include

from .views import (
    no_model_and_rest,
    model_no_rest,
    rest_get,
    rest_post_method,
    rest_one_item,
    RestCBV,
    CBV_pk,
    mixins_list,
    mixins_pk,
    generics_list,
    generics_pk,
    viewsets_guest,
    viewsets_movie,
    viewsets_reservation,
)

from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('guests', viewsets_guest)
router.register('movies', viewsets_movie)
router.register('reservations', viewsets_reservation)

app_name = 'main-app'

urlpatterns = [
    path('no_model_and_rest/', no_model_and_rest, name='no_model_and_rest'),
    path('model_no_rest/', model_no_rest, name='model_no_rest'),
    path('rest_get/', rest_get, name='rest_get'),
    path('rest_post/', rest_post_method, name='rest_post'),
    path('rest_one/<int:pk>/', rest_one_item, name='rest_one_item'),
    path('restcbv/', RestCBV.as_view(), name='rest_cbv'),

    # 4.2 GET PUT DELETE from rest framework class based view APIView
    path('rest/cbv/<int:pk>', CBV_pk.as_view()),

    # 5.1 GET POST from rest framework class based view mixins
    path('rest/mixins/', mixins_list.as_view()),

    # 5.2 GET PUT DELETE from rest framework class based view mixins
    path('rest/mixins/<int:pk>', mixins_pk.as_view()),

    # 6.1 GET POST from rest framework class based view generics
    path('rest/generics/', generics_list.as_view()),

    # 6.2 GET PUT DELETE from rest framework class based view generics
    path('rest/generics/<int:pk>', generics_pk.as_view()),


    # 7 Viewsets
    path('rest/viewsets/', include(router.urls)),

]
