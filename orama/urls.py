from django.urls import path, include
from rest_framework import routers
from freelancer.api import FreelancerViewSet


router = routers.SimpleRouter()
router.register(r'freelancer', FreelancerViewSet, basename='freelancer')

urlpatterns = [
    path('api/', include(router.urls))
]