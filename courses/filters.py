import django_filters as df
from .models import Course

class CourseFilter(df.FilterSet):
    price_min   = df.NumberFilter(field_name='price', lookup_expr='gte')
    price_max   = df.NumberFilter(field_name='price', lookup_expr='lte')
    starts_after = df.DateFilter(field_name='start_date', lookup_expr='gte')
    reg_before   = df.DateFilter(field_name='registration_end_date', lookup_expr='lte')

    class Meta:
        model = Course
        fields = ['is_active']