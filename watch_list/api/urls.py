from django.urls import path, include
from rest_framework.routers import DefaultRouter

from watch_list.api import views

router = DefaultRouter()
router.register("stream", views.StreamPlatformViewSet, basename='streamplatform')

urlpatterns = [
    path('watchlist/', views.WatchListApiView.as_view(), name='watchlist'),
    path('watchlist/<int:pk>/', views.WatchListDetailApiView.as_view(), name='watchlist-detail'),

    # path('stream/', views.StreamPlatformApiView.as_view()),
    # path('stream/<int:pk>/', views.StreamPlatformDetailApiView.as_view()),

    path('', include(router.urls)),

    # path('review/', views.ReviewList.as_view(), name="review-list"),
    # path('review/<int:pk>', views.ReviewDetail.as_view(), name='review-detail')

    path('watchlist/<int:pk>/review/', views.ReviewList.as_view(), name='review-list'),
    path('review/<int:pk>/', views.ReviewDetail.as_view(), name="review-detail"),
    path('watchlist/<int:pk>/review-create/', views.ReviewCreate.as_view(), name="review-create"),

    path('review/', views.UserReview.as_view(), name='user-review-detail'),

    path('watchlist2/', views.WatchListGenericView.as_view(), name='watchlist2'),
]
