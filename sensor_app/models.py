from django.db import models
import time
import uuid

# Create your models here.
class Location(models.Model):
    locId = models.CharField(default=('LOC' + str(uuid.uuid4().int)[:5]), editable=False, unique=True, max_length=50)
    name = models.CharField(max_length=100, default="Name")
    location = models.CharField(max_length=100, default="Location")

    def __str__(self):
        return self.name

class Sensor(models.Model):
    location = models.ForeignKey(Location, related_name='sensors', on_delete=models.CASCADE)
    name = models.CharField(max_length=100, blank=False, null=False)
    sensor_id = models.CharField(max_length=100, blank=False, null=False, unique=True)
    unit = models.CharField(max_length=100, blank=False, null=False)

    def __str__(self):
        return self.name

class LiveSensor(models.Model):
    sensor = models.ForeignKey(Sensor, related_name='live_sensors', on_delete=models.CASCADE)
    data = models.CharField(max_length=100, blank=False, null=False)
    # unit = models.CharField(max_length=100, blank=False, null=False)
    timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)
    # date_time = models.DateTimeField(default=time.time)

    def __str__(self):
        return self.sensor.name

# Blockchain specific models
class Mempool(models.Model):
    sensor_id = models.CharField(default="", max_length=250)
    data = models.CharField(default="", max_length=250)
    timestamp = models.DateTimeField()

class Block(models.Model):
    index = models.IntegerField(default=1)
    nonce = models.IntegerField(default=1)
    merkle_root_hash = models.CharField(max_length=1000, default="0")
    prev_hash = models.CharField(max_length=1000, default="0")
    timestamp = models.DateTimeField()

    def __str__(self):
        return str(self.index)

class Transaction(models.Model):
    block = models.ForeignKey(Block, related_name='block_transactions', on_delete=models.CASCADE)
    txn = models.CharField(default="", max_length=250)

    def __str__(self):
        return f"Block No. {self.block.index}"

class TxnDB1(models.Model):
    block = models.ForeignKey(Block, related_name='block_txnDB1', on_delete=models.CASCADE)
    sensor_id = models.CharField(default="", max_length=250)
    data = models.CharField(default="", max_length=250)
    timestamp = models.DateTimeField()

    def __str__(self):
        return f"Block No. {self.block.index}"

class TxnDB2(models.Model):
    block = models.ForeignKey(Block, related_name='block_txnDB2', on_delete=models.CASCADE)
    sensor_id = models.CharField(default="", max_length=250)
    data = models.CharField(default="", max_length=250)
    timestamp = models.DateTimeField()

    def __str__(self):
        return f"Block No. {self.block.index}"