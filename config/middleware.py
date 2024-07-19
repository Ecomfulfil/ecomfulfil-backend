from django.http import JsonResponse, Http404
import json
import logging

# Setup logging
logger = logging.getLogger(__name__)


class CustomErrorMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        return self.process_response(request, response)

    def format_error_response(self, message, status=400):
        """Utility method to format JSON error responses."""
        return JsonResponse({"error": message}, status=status)

    def process_exception(self, request, exception):
        """Handle exceptions globally with a custom JSON response."""
        if isinstance(exception, Http404):
            return self.format_error_response(
                "The requested resource was not found", 404
            )
        else:
            logger.error("Unhandled server error: %s", exception, exc_info=True)
            return self.format_error_response("An internal server error occurred.", 500)

    def process_response(self, request, response):
        """Process non-exception-based responses for custom handling or additional logging."""
        if response.status_code == 404:
            return self.format_error_response(
                "The requested URL was not found on this server", 404
            )
        elif response.status_code == 400:
            return self.handle_bad_request(response)
        elif response.status_code >= 500:
            return self.format_error_response("Internal server error", 500)

        return response

    def handle_bad_request(self, response):
        """Handles bad request responses to format them properly."""
        try:
            details = json.loads(response.content.decode("utf-8"))
            if "non_field_errors" in details:
                message = (
                    details["non_field_errors"][0]
                    if details["non_field_errors"]
                    else "Bad request with unspecified error."
                )
                return self.format_error_response(message)
            return self.format_error_response(
                "Bad request with unspecified error.", 400
            )
        except json.JSONDecodeError:
            return self.format_error_response("Invalid JSON input", 400)
