from django.contrib import admin
from.models import Ownerreg

class Owneradmin(admin.ModelAdmin):
    list_display=('oid','oname')
    search_fields = ('oid','oname')

admin.site.register(Ownerreg,Owneradmin)

# Register your models here.
