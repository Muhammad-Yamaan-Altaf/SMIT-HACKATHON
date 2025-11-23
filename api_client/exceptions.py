# api_client/exceptions.py

class APIError(Exception):
    """Base exception class for all API errors."""
    pass

class CityNotFoundError(APIError):
    """Raised when the requested city is not found by the API."""
    pass

class APICallFailedError(APIError):
    """Raised for general API request failures (e.g., connection issue, server down)."""
    pass