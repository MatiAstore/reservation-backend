import django_filters
from .models import Reservation

class ReservationFilter(django_filters.FilterSet):
    start_after = django_filters.DateTimeFilter( #nombre query param eg: ?start_after=2026-02-01  
        field_name= "start_date",
        lookup_expr="gte"
    )
    end_before = django_filters.DateTimeFilter(
        field_name= "end_date",
        lookup_expr="lte"
    )

    class Meta:
        model = Reservation
        fields = ["status", "space"] #filtros automaticos es = filterset_fields = ["status", "space"]

     