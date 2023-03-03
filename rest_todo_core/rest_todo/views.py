from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.pagination import PageNumberPagination
from .models import UserPost
from .serializers import UserPostSerializer, CreateUserSerializer
from .permissions import IsOwnerOrReadOnly
from .utils import patch_error_handler

# i'm not completely following API design here, so it is 1:1 matching between HTTP and CRUD
class ListCreateUserPosts(APIView, PageNumberPagination):
    page_size = 5
    serializer_class = UserPostSerializer
    permission_classes = [IsAuthenticatedOrReadOnly,]

    def get(self, request): # all can read
        posts = UserPost.objects.all()
        # pagination works, but doesn't show pagination buttons when using Test page in the Browser
        result_page = self.paginate_queryset(posts, request)
        seralizered_data = self.serializer_class(result_page, many=True)
        response = self.get_paginated_response(seralizered_data.data)
        response.data['posts'] = response.data.pop('results')
        return response

    def post(self, request): # only authenticated user can create
        seraialized_data = self.serializer_class(
            data=request.data, 
            context={'request': request}
        )
        seraialized_data.is_valid(raise_exception=True)
        res = seraialized_data.save()
        headers = {'Location': f'http://{request.get_host()}/api/v1/userpost/{res.id}/'}
        return Response({'post': seraialized_data.data}, status=status.HTTP_201_CREATED, headers=headers)


class GetUpdateDeleteUserPost(APIView):
    serializer_class = UserPostSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly,]

    def get(self, request, pk=None): # for all, because maybe someone wants to check a specific post
        post = get_object_or_404(UserPost, pk=pk)
        seralizered_data = self.serializer_class(post)
        return Response({'post': seralizered_data.data})

    def put(self, request, **kwargs): # only authenticated user and an author of the post
        partial = kwargs.pop('partial', False)
        old_instance = get_object_or_404(UserPost, pk=kwargs.get('pk'))
        self.check_object_permissions(request, old_instance)
        seraialized_data = self.serializer_class(
            data=request.data, 
            instance=old_instance, 
            context={'request': request},
            partial=partial
        )
        seraialized_data.is_valid(raise_exception=True)
        seraialized_data.save()
        return Response(seraialized_data.data)

    @patch_error_handler
    def patch(self, request, **kwargs): # only authenticated user and an author of the post
        # it seems like generic patch doesn't provide any error handling. It returns
        # 200 + an old data per every invalid request that i tried. At leats it doesn't 
        # apply changes
        kwargs['partial'] = True
        return self.put(request, **kwargs)

    def delete(self, request, pk): # only authenticated user and an author of the post
        instance = get_object_or_404(UserPost, pk=pk)
        self.check_object_permissions(request, instance)
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class CreateUser(APIView):
    serializer_class = CreateUserSerializer

    def post(self, request):
        serialized_data = CreateUserSerializer(data=request.data)
        serialized_data.is_valid(raise_exception=True)
        serialized_data.save()
        return Response({'new_user': serialized_data.data}, status=status.HTTP_201_CREATED)
