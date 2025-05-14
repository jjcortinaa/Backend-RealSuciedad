from rest_framework.permissions import BasePermission, SAFE_METHODS
class IsOwnerOrAdmin(BasePermission):
    """
    Permite editar/eliminar una subasta solo si el usuario es el propietario
    o es administrador. Cualquiera puede consultar (GET).
    """
    def has_object_permission(self, request, view, obj):
        # Permitir acceso de lectura a cualquier usuario (GET, HEAD, OPTIONS)
        if request.method in SAFE_METHODS:
            return True
            # Permitir si el usuario es el creador o es administrador
        return obj.auctioneer == request.user or request.user.is_staff
    
class IsAuthenticatedOrReadOnly(BasePermission):
    """
    Permite ver (GET) a cualquier usuario, pero solo permite crear (POST)
    si el usuario está autenticado.
    """
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        return request.user and request.user.is_authenticated
