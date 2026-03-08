from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError 
from django.utils import timezone
import uuid
from core.exceptions import BusinessRuleError, ConflictError

class Reservation(models.Model):
    class Status(models.TextChoices):   
        PENDING = "PEND", "Pendiente"
        ACTIVE = "ACTV", "Activa"
        COMPLETED = "COMP", "Completada"
        CANCELLED = "CANC", "Cancelada"
    
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=5, choices=Status.choices, default=Status.PENDING)
    qr_token = models.UUIDField(
        default= uuid.uuid4,
        editable=False,
        unique=True
    )

    #Relaciones
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete= models.CASCADE,
        related_name = "reservations"
    )

    space = models.ForeignKey(
        "spaces.Space",
        on_delete=models.CASCADE,
        related_name = "reservations"
    )

    class Meta:
        ordering = ["-start_date"]

    def _str__(self):
        return f"{self.user.username} - {self.space.name} ({self.start_date.strftime('%d/%m %H:%M')})"

    def clean(self):
        if self.start_date >= self.end_date:
            raise BusinessRuleError("La fecha de fin debe ser posterior a la fecha de inicio.")
        
        if self.start_date < timezone.now() and not self.pk: # El self.pk para poder actualizar  
            raise BusinessRuleError("No se puede reservar en el pasado")
      
        overlaps = Reservation.objects.filter(
            space=self.space,
            status__in=[self.Status.PENDING, self.Status.ACTIVE],
            start_date__lt=self.end_date,
            end_date__gt=self.start_date
        ).exclude(pk=self.pk) # Excluirme a mí mismo si estoy editando

        if overlaps.exists():
            raise ConflictError("El espacio ya está ocupado en ese rango horario")
    
    def cancel(self):
        if self.status == self.Status.COMPLETED:
            raise BusinessRuleError("No se puede cancelar una reserva completada")
        self.status = self.Status.CANCELLED
