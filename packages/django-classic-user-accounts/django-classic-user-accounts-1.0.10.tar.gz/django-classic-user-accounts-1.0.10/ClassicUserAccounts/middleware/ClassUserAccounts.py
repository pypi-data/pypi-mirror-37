from django.conf import settings
import django
if django.VERSION >= (1, 10):
	from django.utils.deprecation import MiddlewareMixin as BaseMiddleware
else:
	BaseMiddleware = object
	
	
class ClassicUserAccountsMiddleWare(BaseMiddleware):
	def process_request(self, request):
		try:
			if hasattr(settings, 'SITE_NAME'):
				request.site_name = settings.SITE_NAME
		except:
			request.site_name = ''
