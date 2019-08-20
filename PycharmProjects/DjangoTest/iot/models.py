from django.db import models

# Create your models here.


class IOTTest(models.Model):
    sourceIP = models.CharField(max_length=32)
    distIP = models.CharField(max_length=32)
    communicationCunt = models.IntegerField()


class BinaryStore(models.Model):
    timestamp = models.FloatField()
    binaryData = models.BinaryField()


class FieldsInfo(models.Model):
    timestamp = models.FloatField()
    eth_src = models.BinaryField(max_length=6)
    eth_dst = models.BinaryField(max_length=6)
    eth_type = models.IntegerField()
    ip_src = models.BinaryField(max_length=16)
    ip_dst = models.BinaryField(max_length=16)
    ip_proto = models.IntegerField()
    trans_sport = models.IntegerField()
    trans_dport = models.IntegerField()
