from rest_framework import generics
from rest_framework import status
from rest_framework import views
from rest_framework import viewsets
# from rest_framework.authentication import BasicAuthentication, SessionAuthentication
# from rest_framework.authentication import TokenAuthentication
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.throttling import AnonRateThrottle, UserRateThrottle, ScopedRateThrottle
from rest_framework import filters

from django_filters.rest_framework import DjangoFilterBackend

from watch_list.api import permissions
from watch_list.api import serializers
from watch_list.models import WatchList, StreamPlatform, Review
from watch_list.api import throttling
from watch_list.api import pagination


class WatchListGenericView(generics.ListAPIView):
    serializer_class = serializers.WatchListSerializer
    queryset = WatchList.objects.all()
    permission_classes = [AllowAny]
    # pagination_class = pagination.WatchListPagination
    pagination_class = pagination.WatchListCursorPagination
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = 'heavy-user-throttle'


class WatchListApiView(views.APIView):

    permission_classes = [permissions.IsAdminOrReadOnly]

    def get(self, request, format=None):
        watch_lists = WatchList.objects.all()
        serializer = serializers.WatchListSerializer(watch_lists, many=True)

        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = serializers.WatchListSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class WatchListDetailApiView(views.APIView):

    permission_classes = [permissions.IsAdminOrReadOnly]

    def get(self, request, format=None, pk=None):
        try:
            watch_list = WatchList.objects.get(pk=pk)
        except WatchList.DoesNotExist:
            return Response("Watch List Does Not Exist", status=status.HTTP_404_NOT_FOUND)

        serializer = serializers.WatchListSerializer(watch_list)
        return Response(serializer.data)

    def put(self, request, format=None, pk=None):

        try:
            watch_list = WatchList.objects.get(pk=pk)
        except WatchList.DoesNotExist:
            return Response("Watch List Does Not Exist", status=status.HTTP_404_NOT_FOUND)

        serializer = serializers.WatchListSerializer(watch_list, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, format=None, pk=None):
        try:
            watch_list = WatchList.objects.get(pk=pk)
        except WatchList.DoesNotExist:
            return Response("Watch List Does Not Exist", status=status.HTTP_404_NOT_FOUND)

        watch_list.delete()
        return Response("Watch List Deleted Successfully")


class StreamPlatformApiView(views.APIView):

    permission_classes = [permissions.IsAdminOrReadOnly]

    def get(self, request, format=None):
        streaming_platforms = StreamPlatform.objects.all()
        # context={'request': request}
        serializer = serializers.StreamPlatformSerializer(streaming_platforms, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):

        serializer = serializers.StreamPlatformSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class StreamPlatformDetailApiView(views.APIView):

    permission_classes = [permissions.IsAdminOrReadOnly]

    def get(self, request, format=None, pk=None):

        try:
            stream_platform = StreamPlatform.objects.get(pk=pk)
        except StreamPlatform.DoesNotExist:
            return Response("Stream Platform Does Not Exists", status=status.HTTP_404_NOT_FOUND)

        serializer = serializers.StreamPlatformSerializer(stream_platform)

        return Response(serializer.data)

    def put(self, request, format=None, pk=None):

        try:
            stream_platform = StreamPlatform.objects.get(pk=pk)
        except StreamPlatform.DoesNotExist:
            return Response("Stream Platform Does Not Exists", status=status.HTTP_404_NOT_FOUND)

        serializer = serializers.StreamPlatformSerializer(stream_platform, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, format=None, pk=None):

        try:
            stream_platform = StreamPlatform.objects.get(pk=pk)
        except StreamPlatform.DoesNotExist:
            return Response("Stream Platform Does Not Exists", status=status.HTTP_404_NOT_FOUND)

        stream_platform.delete()
        return Response("Stream Platform Deleted Successfully")


# # Using viewset for StreamPlatform
# class StreamPlatformViewSet(viewsets.ViewSet):
#
#     def list(self, request):
#         queryset = StreamPlatform.objects.all()
#         serializer = serializers.StreamPlatformSerializer(queryset, many=True)
#         return Response(serializer.data)
#
#     def retrieve(self, request, pk=None):
#         queryset = StreamPlatform.objects.all()
#         stream_platform = get_object_or_404(queryset, pk=pk)
#         serializer = serializers.StreamPlatformSerializer(stream_platform)
#         return Response(serializer.data)
#
#     def create(self,request):
#         serializer = serializers.StreamPlatformSerializer(data=request.data)
#
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         else:
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#     def destroy(self, request,pk=None):
#         try:
#             stream_platform = StreamPlatform.objects.get(pk=pk)
#         except StreamPlatform.DoesNotExist:
#             return Response("Stream Platform Does Not Exists", status=status.HTTP_404_NOT_FOUND)
#
#         stream_platform.delete()
#         return Response("Stream Platform Deleted Successfully")

# using Model ViewSet for Stream Platform
class StreamPlatformViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.StreamPlatformSerializer
    queryset = StreamPlatform.objects.all()
    permission_classes = [permissions.IsAdminOrReadOnly]


# # generics and mixins based views
# class ReviewList(mixins.ListModelMixin,
#                  mixins.CreateModelMixin,
#                  generics.GenericAPIView):
#
#     queryset = Review.objects.all()
#     serializer_class = serializers.ReviewSerializer
#
#     def get(self, request, *args, **kwargs):
#         return self.list(request, *args, **kwargs)
#
#     def post(self, request, *args, **kwargs):
#         return self.create(request, *args, **kwargs)
#
#
# class ReviewDetail(mixins.RetrieveModelMixin,
#                    generics.GenericAPIView):
#
#     queryset = Review.objects.all()
#     serializer_class = serializers.ReviewSerializer
#
#     def get(self, request, *args, **kwargs):
#         return self.retrieve(request, *args, **kwargs)


# using generic class based views
class ReviewList(generics.ListAPIView):
    # queryset = Review.objects.all()
    serializer_class = serializers.ReviewSerializer
    permission_classes = [AllowAny]
    throttle_classes = [throttling.ReviewListThrottling]
    # Not required since we have already defined it in settings.py
    # authentication_classes = [TokenAuthentication]
    # filter_backends = [DjangoFilterBackend]
    filterset_fields = ['rating', 'review_user__username', 'is_active']
    filter_backends = [filters.SearchFilter,filters.OrderingFilter]
    search_fields = ['rating', 'review_user__username', 'is_active']
    ordering_fields = ['rating']

    def get_queryset(self):
        pk = self.kwargs['pk']
        return Review.objects.filter(watchlist=pk)


class ReviewDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Review.objects.all()
    serializer_class = serializers.ReviewSerializer
    # permission_classes = [IsAuthenticatedOrReadOnly]
    # permission_classes = [permissions.IsAdminOrReadOnly]
    permission_classes = [permissions.IsReviewUserOrReadOnly]
    # throttle_classes = [throttling.ReviewDetailThrottling]
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = 'review-detail'


class ReviewCreate(generics.CreateAPIView):
    queryset = Review.objects.all()
    serializer_class = serializers.ReviewSerializer

    def perform_create(self, serializer):
        pk = self.kwargs.get('pk')
        watchlist = WatchList.objects.get(pk=pk)

        review_user = self.request.user
        review_queryset = Review.objects.filter(watchlist=watchlist, review_user=review_user)

        if review_queryset.exists():
            raise ValidationError("You have already Submitted Review for this watchlist")

        if watchlist.number_rating == 0:
            watchlist.avg_rating = serializer.validated_data['rating']
        else:
            watchlist.avg_rating = (watchlist.avg_rating + serializer.validated_data['rating']) / 2

        watchlist.number_rating = watchlist.number_rating + 1
        watchlist.save()

        serializer.save(watchlist=watchlist, review_user=review_user)


class UserReview(generics.ListAPIView):
    serializer_class = serializers.ReviewSerializer
    permission_classes = [permissions.IsAdminOrReadOnly]

    # def get_queryset(self):
    #     # here 'username' in self.kwargs is for the url param
    #     username = self.kwargs['username']
    #     # here we have to use __ because review_user is a ForeignKey and username is a field of User class
    #     return Review.objects.filter(review_user__username=username)

    def get_queryset(self):
        username = self.request.query_params.get('username')
        return Review.objects.filter(review_user__username=username)

