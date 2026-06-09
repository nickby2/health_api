from rest_framework.routers import DefaultRouter

from appointments.views.appointment_viewset import AppointmentViewSet

router = DefaultRouter()
router.register(r"appointments", AppointmentViewSet, basename="appointment")

urlpatterns = router.urls
