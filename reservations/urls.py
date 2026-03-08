from rest_framework import routers 
from .api import ReservationViewSet

router = routers.DefaultRouter()
router.register("api/v1/reservations", ReservationViewSet, basename="reservations")

urlpatterns = router.urls