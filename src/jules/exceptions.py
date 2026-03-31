class JulesError(Exception):
    """Base error for the Jules SDK"""
    pass

class AuthError(JulesError):
    """Raised on authentication failures (401/403)"""
    pass

class RateLimitError(JulesError):
    """Raised when hitting API rate limits (429)"""
    pass

class NotFoundError(JulesError):
    """Raised when a resource is not found (404)"""
    pass

class IdempotencyConflict(JulesError):
    """Raised on 409 conflict for source_event_id"""
    pass

class TransportError(JulesError):
    """Raised for underlying HTTP/network issues"""
    pass
