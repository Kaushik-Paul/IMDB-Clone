from rest_framework import serializers

from watch_list.models import WatchList, StreamPlatform, Review


class ReviewSerializer(serializers.ModelSerializer):

    review_user = serializers.CharField(read_only=True)

    class Meta:
        model = Review
        # fields = "__all__"
        exclude = ("watchlist",)


class WatchListSerializer(serializers.ModelSerializer):
    # reviews = ReviewSerializer(many=True, read_only=True)
    # platform = serializers.CharField()

    class Meta:
        model = WatchList
        # fields = ['id', 'title', 'description', 'platform', 'is_active', 'created_on', 'updated_on']
        fields = "__all__"


class StreamPlatformSerializer(serializers.ModelSerializer):
    # watchlist = WatchListSerializer(many=True, read_only=True)

    watchlist = serializers.StringRelatedField(many=True, read_only=True)
    # watchlist = serializers.HyperlinkedRelatedField(
    #     many=True,
    #     read_only=True,
    #     view_name='watchlist-detail'
    # )

    class Meta:
        model = StreamPlatform
        fields = "__all__"
