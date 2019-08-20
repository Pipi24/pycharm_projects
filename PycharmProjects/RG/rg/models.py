from django.db import models


# Create your models here.


class FieldsInfo(models.Model):
    timestamp = models.FloatField()
    eth_src = models.CharField(max_length=32)
    eth_dst = models.CharField(max_length=32)
    eth_type = models.CharField(max_length=32)
    ip_src = models.CharField(max_length=64)
    ip_dst = models.CharField(max_length=64)
    ip_proto = models.CharField(max_length=32)
    trans_sport = models.IntegerField()
    trans_dport = models.IntegerField()
    comm_way = models.CharField(max_length=32, null=True, default='Unknown')


class IpHost(models.Model):
    ip = models.CharField(max_length=64)
    host = models.CharField(max_length=64)


class RgBaseInfo(models.Model):
    timestamp = models.FloatField()
    eth_src = models.CharField(max_length=32)
    eth_dst = models.CharField(max_length=32)
    eth_type = models.CharField(max_length=32)
    ip_src = models.CharField(max_length=64)
    ip_dst = models.CharField(max_length=64)
    ip_proto = models.CharField(max_length=32)
    trans_sport = models.IntegerField()
    trans_dport = models.IntegerField()
    comm_way = models.CharField(max_length=32, null=True, default='Unknown')
    host_src = models.CharField(max_length=64, null=True)
    host_dst = models.CharField(max_length=64, null=True)
