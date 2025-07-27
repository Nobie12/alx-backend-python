# chats/middleware.py
from django.http import HttpResponseForbidden
import logging
from datetime import datetime, timedelta
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

class RolePermissionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        protected_paths = [
            "/api/messages/delete",  # Add specific admin/moderator endpoints here
            "/api/messages/update",
        ]

        if request.path in protected_paths:
            user = request.user

            if not user.is_authenticated:
                return JsonResponse({
                    "error": "Authentication required."
                }, status=403)

            # Check for role: assume user has a `role` attribute
            role = getattr(user, 'role', None)

            if role not in ['admin', 'moderator']:
                return JsonResponse({
                    "error": "You do not have permission to perform this action."
                }, status=403)

        return self.get_response(request)
