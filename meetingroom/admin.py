from django.contrib import admin
from .models import MeetingRoomEquipment, MeetingRoomInfos, MeetRoomReserve
# Register your models here.

@admin.register(MeetingRoomEquipment)
class MeetingRoomEquipmentAdmin(admin.ModelAdmin):
    pass


@admin.register(MeetingRoomInfos)
class MeetingRoomInfosAdmin(admin.ModelAdmin):
    pass


@admin.register(MeetRoomReserve)
class MeetRoomReserveAdmin(admin.ModelAdmin):
    pass