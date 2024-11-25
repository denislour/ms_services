from sanic.handlers import ErrorHandler as BaseErrorHandler
from sanic.response import json
from pydantic import ValidationError

class ErrorHandler(BaseErrorHandler):
    def default(self, request, exception):
        # Handle Pydantic validation errors
        if isinstance(exception, ValidationError):
            return json(
                {
                    "error": "Validation Error",
                    "detail": exception.errors()
                },
                status=400
            )
            
        # Handle 404 errors
        if hasattr(exception, "status_code") and exception.status_code == 404:
            return json(
                {
                    "error": "Not Found",
                    "message": str(exception)
                },
                status=404
            )
            
        # Handle other errors
        return json(
            {
                "error": "Internal Server Error",
                "message": str(exception)
            },
            status=500
        )
