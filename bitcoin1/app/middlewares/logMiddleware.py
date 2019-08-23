from django.http import request
from django.shortcuts import redirect
from django.utils.deprecation import MiddlewareMixin


class LogMiddleware(MiddlewareMixin):
    def process_request(self,request):
        if request.path not in ['/login/','/verifycode/'] :
            username = request.session.get('username')
            if not username:
                return redirect('/login/')
        return None

#
# class LogMiddleware(MiddlewareMixin):
#     def process_request(self):
#         if request.path in :
#             return redirect('/login/')




