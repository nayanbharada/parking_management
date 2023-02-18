from django.contrib import admin
from parking_premises.models import Premises, Slot, BookParking
# Register your models here.

admin.site.register(Premises)
admin.site.register(Slot)
admin.site.register(BookParking)