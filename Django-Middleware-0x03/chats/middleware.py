# chats/middleware.py

import logging
from datetime import datetime

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
