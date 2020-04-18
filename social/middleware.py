import datetime

from .models import Logger
from django.utils.deprecation import MiddlewareMixin

class log_request(MiddlewareMixin):
    def process_response(self, request, response):

        if request.user.is_authenticated:
            oLogger_data = Logger()
            oLogger_data.oDate = datetime.datetime.now().date()
            oLogger_data.nUser_id = request.user

            if request.path in ('/api/post/', 'api/like/', 'api/analitics/'):
                oRecord_log = Logger.objects.filter(nUser_id=request.user, aAction='request').first()
                oLogger_data.aAction = 'request'
                if oRecord_log is not None:
                    oLogger_data.id = oRecord_log.id
                    oLogger_data.save(force_update=True)
                else:
                    oLogger_data.save()

            if request.path in ('/api/login/'):
                oRecord_log = Logger.objects.filter(nUser_id=request.user, aAction='login').first()
                oLogger_data.aAction = 'login'
                if oRecord_log is not None:
                    oLogger_data.id = oRecord_log.id
                    oLogger_data.save(force_update=True)
                else:
                    oLogger_data.save()

        return response
