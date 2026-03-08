class DomainError(Exception):
    pass 

class BusinessRuleError(DomainError):
    """Violación de una regla de negocio"""
    pass


class PermissionDeniedError(DomainError):
    """El actor no puede hacer esto"""
    pass


class NotFoundError(DomainError):
    """Entidad inexistente en el dominio"""
    pass


class ConflictError(DomainError):
    """Estado incompatible (overlap, duplicado, etc)"""
    pass