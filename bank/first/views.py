import logging
import zlib
import requests
from rest_framework.views import APIView
from first.models import CurRate
from rest_framework.response import Response

cur_list = {}
logger = logging.getLogger(__name__)


class CurAPIView(APIView):
    def get(self, request):
        try:
            CurAPIView.createRows(request)
            logger.info(f'Request : {request.__dict__["_request"]}.Response: успешно!')
            return Response('Данные были успешно загружены в бд.',status=200,headers={'CRC32': zlib.crc32(bytes(str('checksum'), 'UTF-8'))})
        except AttributeError:
            return Response('Ошибка во время добавления данных. Проверьте входные данные.',status=404)

    @staticmethod
    def getCurID(date) -> None:
        global cur_list
        r = requests.get('https://www.nbrb.by/api/exrates/currencies')  # For cur_id
        temp = [x['Cur_ID'] for x in r.json() if x['Cur_DateEnd'] == '2050-01-01T00:00:00']
        for x in temp:
            r = requests.get(f'https://www.nbrb.by/api/exrates/rates/{x}?ondate={date}')
            cur_list[x] = r.json()

    @staticmethod
    def createRows(request):
        CurAPIView.getCurID(request.GET['date'])
        for x in cur_list.values():
            CurRate.objects.create(Cur_ID=x['Cur_ID']
                                   , Date=x['Date']
                                   , Cur_Abbreviation=x['Cur_Abbreviation']
                                   , Cur_Scale=x['Cur_Scale']
                                   , Cur_Name=x['Cur_Name']
                                   , Cur_OfficialRate=x['Cur_OfficialRate'])
        cur_list.clear()
