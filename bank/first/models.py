from django.db import models


class CurRate(models.Model):
    Cur_ID = models.IntegerField(default=0, null=False)
    Date = models.DateTimeField(null=True)
    Cur_Abbreviation = models.CharField(max_length=3,null=True)
    Cur_Scale = models.IntegerField(default=1)
    Cur_Name = models.CharField(max_length=255,null=True)
    Cur_OfficialRate = models.FloatField(null=True)
