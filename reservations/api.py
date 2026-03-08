from .models import Reservation
from .services import reservation_service
from .permissions import IsOwnerOrAdmin
from .serializers import ReservationSerializer, ReservationCalendarSerializer
from .filters import ReservationFilter
from .pagination import ReservationPagination
from rest_framework import viewsets
from rest_framework.decorators import action
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response
from rest_framework import status 
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import filters
from rest_framework.exceptions import ValidationError
from users.models import User

class ReservationViewSet(viewsets.ModelViewSet):
    queryset = Reservation.objects.all() 
    serializer_class = ReservationSerializer #serializador de la reserva
    permission_classes = [IsAuthenticated] 
    pagination_class = ReservationPagination #paginacion custom para limit
    filterset_class = ReservationFilter

    # Filtros para la lista de reservas
    filter_backends = [ 
        DjangoFilterBackend,
        filters.OrderingFilter,
    ]
    ordering_fields = ["start_date", "created_at"]
    ordering = ["-start_date"]

    def get_queryset(self):
        user = self.request.user
      
        if user.role in ["ADMIN", "MAINTENANCE"]: 
            return Reservation.objects.all()
        return Reservation.objects.filter(user=user)

    @action(detail=True, methods=["POST"], permission_classes=[IsOwnerOrAdmin])
    def cancel(self, request, pk=None):
        reservation = self.get_object() 
        reservation_service.ReservationService().cancel_reservation(reservation)
        return Response(
            {"detail": "Reserva cancelada"},
            status=status.HTTP_200_OK
        )

    @action(detail=False, methods=["GET"])
    def calendar(self, request):
        start_after = request.query_params.get("start_after") 
        end_before = request.query_params.get("end_before")

        if not start_after or not end_before: 
            raise ValidationError(
                "Debe proporcionar los parámetros 'start_after' y 'end_before' para el calendario."
            )

        # Reutilizamos el filtro existente para status/space y rango
        base_qs = Reservation.objects.all() 
        filtered_qs = ReservationFilter( 
            data=request.query_params,
            queryset=base_qs,
        ).qs

        serializer = ReservationCalendarSerializer(
            filtered_qs,
            many=True
        )
        return Response(serializer.data)



