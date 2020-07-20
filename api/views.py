from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet, ViewSet
from django.contrib.auth import get_user_model
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings
from api.permissions import *
from api.serializers import *
from api.models import *
from rest_framework.response import Response
from rest_framework import generics
from rest_framework.routers import SimpleRouter
from rest_framework.urlpatterns import format_suffix_patterns
from collections import OrderedDict
from rest_framework.reverse import reverse
from rest_framework import renderers
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
# Create your views here.
User = get_user_model()
class UserViewSet(ModelViewSet):
    serializer_class = UserModelSerializer
    queryset = User.objects.all()
    permission_classes = (IsAuthenticated, UserUpdatePermission, )
    authentication_classes = (TokenAuthentication, )


class MovieViewSet(ModelViewSet):
    serializer_class = MovieSerializer
    queryset = Movie.objects.all()
    permission_classes = (AdminAuthenticationPermission, )
    authentication_classes = (TokenAuthentication, )

    def perform_create(self, serializer):
        serializer.save(num_ratings = 0, avg_rating = 0)


class UserLoginApiView(ObtainAuthToken):
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES
    template_name = 'rest_framework/login.html'
    def get(self, request, *args, **kwargs):
        return Response(template_name = 'rest_framework/login.html')
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user_id': user.pk,
            'email': user.email
        }, template_name = 'rest_framework/login.html')




class ReviewViewSet(ModelViewSet):
    serializer_class = ReviewSerializer
    queryset = Review.objects.all()
    permission_classes = (IsAuthenticatedOrReadOnly, ReviewPermission, )
    authentication_classes = (TokenAuthentication, )

    def perform_create(self, serializer):
        serializer.save(reviewer = self.request.user)

router = SimpleRouter()
router.register('users',UserViewSet)
router.register('movies',MovieViewSet)
router.register('reviews',ReviewViewSet)


class ApiRootView(generics.GenericAPIView):

    api_root_dict = OrderedDict()
    list_name = router.routes[0].name
    for prefix, viewset, basename in router.registry:
        api_root_dict[prefix] = list_name.format(basename=basename)



    def get(self, request, *args, **kwargs):
        # Return a plain {"name": "hyperlink"} response.
        ret = OrderedDict()
        namespace = request.resolver_match.namespace
        for key, url_name in self.api_root_dict.items():
            if namespace:
                url_name = namespace + ':' + url_name
            ret[key] = reverse(
            url_name,
            args=args,
            kwargs=kwargs,
            request=request,
            format=kwargs.get('format', None)
                )
            ret['login'] = request.build_absolute_uri('login/')


        return Response(ret)
