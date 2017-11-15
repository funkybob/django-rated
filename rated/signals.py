
from django.dispatch import Signal

rate_limited = Signal(providing_args=['client'])
