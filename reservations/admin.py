from django.contrib import admin
from .models import Reservation

@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = ("id", "user","space", "start_date", "end_date", "status")
    list_filter = ("status", "start_date", "end_date", "space", "user")
    search_fields = ("space__name", "user__username", "qr_token")
    readonly_fields = ("qr_token", "created_at")