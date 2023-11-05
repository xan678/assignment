import logging
from datetime import datetime
from .models import URLUsageLog

class ShortURLLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        print(request)
        ip_address = self.get_client_ip(request)
        user_agent = request.META.get('HTTP_USER_AGENT', "")

        self.log_request(ip_address, user_agent)
        response = self.get_response(request)
        return response

    
    def get_client_ip(self, request):
        x_forwared_for = request.META.get('HTTP_X_FORWARDED_FOR')

        if x_forwared_for:
            ip = x_forwared_for.split(',')[0]
        
        else:
            ip = request.META.get('REMOTE_ADDR')
        
        return ip
    
    def log_request(self, ip_address, user_agent):
        logger = logging.getLogger('short_url_logger')
        logger.info(f"AccessTime: {datetime.now()}, IP Address : {ip_address}, User Agent: {user_agent}")