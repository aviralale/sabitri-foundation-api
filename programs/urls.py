from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    ProjectViewSet,
    ProjectImageViewSet,
    PartnerViewSet,
    ProjectPhaseViewSet,
    ProjectOutcomeViewSet,
    TagViewSet,
)

router = DefaultRouter()
router.register(r"projects", ProjectViewSet)
router.register(r"images", ProjectImageViewSet)
router.register(r"partners", PartnerViewSet)
router.register(r"phases", ProjectPhaseViewSet)
router.register(r"outcomes", ProjectOutcomeViewSet)
router.register(r"tags", TagViewSet)

urlpatterns = [
    path("", include(router.urls)),
]
