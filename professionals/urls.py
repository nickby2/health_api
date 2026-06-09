from rest_framework.routers import DefaultRouter

from professionals.views import ProfessionalViewSet

router = DefaultRouter()
router.register(r"professionals", ProfessionalViewSet, basename="professional")

urlpatterns = router.urls