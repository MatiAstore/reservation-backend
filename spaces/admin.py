from django.contrib import admin
from .models import Space, SpaceType, Device, Sensor, SensorType

# Inline para Sensores (se verá dentro de Device)
class SensorInline(admin.TabularInline):
    model = Sensor
    extra = 1 
    fields = ('name', 'identifier', 'sensor_type', 'status', 'last_value')

# 2. Inline para Dispositivos (se verá dentro de Space)
class DeviceInline(admin.StackedInline): # Stacked ocupa más espacio, ideal para dispositivos
    model = Device
    extra = 0
    show_change_link = True # Crea un botoncito para ir al detalle del dispositivo

@admin.register(Space)
class SpaceAdmin(admin.ModelAdmin):
    list_display = ('name', 'space_type', 'location', 'capacity', 'current_status', 'is_active')
    list_filter = ('space_type', 'current_status', 'is_active')
    search_fields = ('name', 'location')
    inlines = [DeviceInline]

@admin.register(Device)
class DeviceAdmin(admin.ModelAdmin):
    list_display = ('name', 'identifier', 'space', 'status', 'last_seen')
    list_filter = ('status', 'space')
    search_fields = ('name', 'identifier')
    inlines = [SensorInline]

@admin.register(Sensor)
class SensorAdmin(admin.ModelAdmin):
    list_display = ('name', 'identifier', 'device', 'sensor_type', 'status', 'last_value')
    list_filter = ('status', 'sensor_type', 'device__space')
    search_fields = ('name', 'identifier')

admin.site.register(SpaceType)
admin.site.register(SensorType)