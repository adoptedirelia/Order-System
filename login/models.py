from django.db import models

# Create your models here.

class PacketInfo(models.Model):   #在mysql数据库里，创建一个表格（名字为PacketInfo）
    name = models.CharField(max_length=64)  #表格里的其中一个字段为name（流量名称）
    type = models.CharField(max_length=64)    #表格里的其中一个字段为type（流量类型）
    desc = models.CharField(max_length=64)
