from rest_framework.throttling import UserRateThrottle


class ReviewListThrottling(UserRateThrottle):
    scope = 'review-list'


class ReviewDetailThrottling(UserRateThrottle):
    scope = 'review-detail'
