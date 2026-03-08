from django.db import models

class SpaceType(models.Model):
    name = models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

class SensorType(models.Model):
    name = models.CharField(max_length=50, unique=True)
    unit = models.CharField(max_length=10, blank=True)

    def __str__(self):
        return f"{self.name} ({self.unit})"

class Space(models.Model):
    class Status(models.TextChoices):
        AVAILABLE = 'AVAIL', 'Disponible'
        RESERVED = 'RESV', 'Reservado'
        OCCUPIED_NO_RES = 'OCCUNR', 'Ocupado sin reserva'
        RESERVED_OCCUPIED = 'RESOCC', 'Reservado y ocupado'
        MAINTENANCE = 'MAINT', 'Mantenimiento'

    name = models.CharField(max_length=100)
    capacity = models.PositiveIntegerField(default=1) 
    location = models.CharField(max_length=255)
    current_status = models.CharField(max_length=10, choices=Status.choices, default=Status.AVAILABLE)
    is_active = models.BooleanField(default=True)
    
    space_type = models.ForeignKey(SpaceType, on_delete=models.PROTECT)
    
    def __str__(self):
        return f"{self.name} ({self.get_current_status_display()})"

class Device(models.Model):
    class Status(models.TextChoices):
        ONLINE = "ON", "Activo"
        OFFLINE = "OFF", "Inactivo"
        MAINTENANCE = "MNT", "Mantenimiento"
        ERROR = "ERR", "Error"

    name = models.CharField(max_length=100)
    identifier = models.CharField(max_length=50, unique=True)
    status = models.CharField(max_length=3, choices=Status.choices, default=Status.OFFLINE) # Corregido choices
    last_seen = models.DateTimeField(auto_now=True)
    
    space = models.ForeignKey(Space, on_delete=models.CASCADE, related_name='devices')
    
    def __str__(self):
        return f"{self.name} ({self.identifier})"

class Sensor(models.Model):
    class Status(models.TextChoices):
        ONLINE = "ON", "Activo"
        OFFLINE = "OFF", "Inactivo"
        MAINTENANCE = "MNT", "Mantenimiento"
        ERROR = "ERR", "Error"

    name = models.CharField(max_length=100)
    identifier = models.CharField(max_length=50, unique=True)
    status = models.CharField(max_length=3, choices=Status.choices, default=Status.OFFLINE)
    last_value = models.FloatField(null=True, blank=True)
    last_seen = models.DateTimeField(auto_now=True) # Sugerencia: auto_now

    device = models.ForeignKey(Device, on_delete=models.CASCADE, related_name="sensors")
    sensor_type = models.ForeignKey(SensorType, on_delete=models.PROTECT)

    def __str__(self):
        return f"{self.name} - {self.identifier}"