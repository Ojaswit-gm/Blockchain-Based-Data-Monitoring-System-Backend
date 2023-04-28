from django.contrib import admin

# Register your models here.
from .models import Sensor, LiveSensor, Location, Mempool, Transaction, Block, TxnDB1, TxnDB2
admin.site.register(Sensor)
# admin.site.register(LiveSensor)
admin.site.register(Location)
admin.site.register(Mempool)
# admin.site.register(Transaction)
admin.site.register(TxnDB1)
admin.site.register(TxnDB2)
admin.site.register(Block)
