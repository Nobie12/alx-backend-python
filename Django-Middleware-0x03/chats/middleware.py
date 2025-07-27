# chats/middleware.py
from django.http import HttpResponseForbidden
import logging
from datetime import datetime
from django.http import JsonResponse

class RequestLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

        # Setup logger
        self.logger = logging.getLogger('request_logger')
        self.logger.setLevel(logging.INFO)

        handler = logging.FileHandler('requests.log')
        formatter = logging.Formatter('%(message)s')
        handler.setFormatter(formatter)

        # Avoid adding multiple handlers if reloading
        if not self.logger.handlers:
            self.logger.addHandler(handler)

    def __call__(self, request):
        user = request.user if request.user.is_authenticated else "AnonymousUser"
        log_entry = f"{datetime.now()} - User: {user} - Path: {request.path}"
        self.logger.info(log_entry)

        response = self.get_response(request)
        return response

class RestrictAccessByTimeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        current_hour = datetime.now().hour  # 24-hour format (0–23)

        # Allow access only between 18:00 (6 PM) and 21:00 (9 PM)
        if current_hour < 18 or current_hour > 21:
            return HttpResponseForbidden(
                "<h1>403 Forbidden</h1><p>Access to the messaging app is restricted outside 6 PM to 9 PM.</p>"
            )

        return self.get_response(request)


# In-memory message log (IP -> [timestamps])
MESSAGE_LOG = {}

class OffensiveLanguageMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Only monitor POST requests to messaging endpoint
        if request.method == 'POST' and request.path.startswith('/api/messages'):
            ip = self._get_client_ip(request)
            now = datetime.now()

            # Get or initialize timestamp list for this IP
            timestamps = MESSAGE_LOG.get(ip, [])

            # Remove timestamps older than 1 minute
            one_minute_ago = now - timedelta(minutes=1)
            timestamps = [t for t in timestamps if t > one_minute_ago]

            if len(timestamps) >= 5:
                return JsonResponse({
                    "error": "Rate limit exceeded. Max 5 messages per minute allowed."
                }, status=429)

            # Log current message
            timestamps.append(now)
            MESSAGE_LOG[ip] = timestamps

        return self.get_response(request)

    def _get_client_ip(self, request):
        """Helper to get IP from request."""
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip