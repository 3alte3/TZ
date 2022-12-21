import datetime
import urllib
import requests
from rest_framework.views import APIView
from rest_framework.response import Response
import zlib
import logging


logger = logging.getLogger(__name__)


class CurOnDateAPIView(APIView):
    def get(self, request, **kwargs):
        try:
            link = f'https://www.nbrb.by/api/exrates/rates/{kwargs.get("cur_id")}?ondate={kwargs.get("date")}'
            dateForCalc = datetime.datetime.strptime(kwargs.get('date'),'%Y-%m-%d') - datetime.timedelta(days=1)
            response = requests.get(link).json()

            linkForCalc = f'https://www.nbrb.by/api/exrates/rates/{kwargs.get("cur_id")}?ondate={dateForCalc}'
            responseForCalc = requests.get(linkForCalc).json()

            differ = response['Cur_OfficialRate'] - responseForCalc['Cur_OfficialRate']


            if differ > 0:
                response.update({'Разница':f'Курс увеличился на {differ}'})
            elif differ == 0 :
                response.update({'Разница': f'Курс не изменился'})
            else :
                response.update({'Разница': f'Курс уменьшился на {differ}'})
            logger.info(f'Request : {request.__dict__["_request"]}.Response: {response}')
            return Response(response, status=200, headers={'CRC32': zlib.crc32(bytes(str(response), 'UTF-8'))})

        except urllib.error.HTTPError:
            return Response('Введены некорректные данные. Пожалуйста, повторите запрос', status=404)

