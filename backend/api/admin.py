from django.contrib import admin

from api.models import *

# Register your models here.

admin.site.register(Team)
admin.site.register(Player)
admin.site.register(PlayerInfo)
admin.site.register(PlayerInfo_Team)
admin.site.register(PlayerRole)
