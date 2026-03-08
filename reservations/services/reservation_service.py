from ..models import Reservation 
from core.exceptions import BusinessRuleError
from django.db import transaction
from spaces.models import Space

class ReservationService:
    @transaction.atomic
    def create_reservation(self, *, user, space, start_date, end_date):
        # Bloquear el espacio concurrentemente para evitar Race Conditions (doble reserva)
        space = Space.objects.select_for_update().get(pk=space.pk)
        
        if not space.is_active:
            raise BusinessRuleError("El espacio está inactivo")

        reservation = Reservation(
            user=user,
            space=space,
            start_date=start_date,
            end_date=end_date,
            status=Reservation.Status.PENDING
        )
        
        reservation.clean()
        reservation.save()
        return reservation

    @transaction.atomic
    def update_reservation(self, reservation, data):
        # Bloquear la reserva y el espacio en caso de modificación de fechas o espacio
        reservation = Reservation.objects.select_for_update().get(pk=reservation.pk)
        
        if reservation.status in [Reservation.Status.COMPLETED, Reservation.Status.CANCELLED]:
            raise BusinessRuleError("No se puede modificar una reserva completada o cancelada")

        for attr, value in data.items():
            setattr(reservation, attr, value)  # instance.space = valor
        reservation.clean()
        reservation.save()
        return reservation

    def cancel_reservation(self, reservation):
        reservation.cancel()
        reservation.save()
        return reservation

