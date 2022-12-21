from rest_framework import serializers
from first.models import CurRate


class CurRateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CurRate
        fields = ('Cur_ID', 'Date', 'Cur_Abbreviation', 'Cur_Scale', 'Cur_Name', 'Cur_OfficialRate',)
