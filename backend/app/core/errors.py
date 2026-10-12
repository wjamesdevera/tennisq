class DomainError(Exception):
    """Base class for all expected business errors."""
    code = "DOMAIN_ERROR"

    def __init__(self, message: str | None = None):
        self.message = message or self.default_message
        super().__init__(self.message)

    default_message = "Something went wrong."


class NotFoundError(DomainError):
    code = "NOT_FOUND"
    default_message = "Resource not found."


class AlreadyExistsError(DomainError):
    code = "ALREADY_EXISTS"
    default_message = "Resource already exists."


class PermissionDeniedError(DomainError):
    code = "PERMISSION_DENIED"
    default_message = "You don't have permission to do this."


class BusinessRuleError(DomainError):
    code = "BUSINESS_RULE_VIOLATION"
    default_message = "This action isn't allowed."
