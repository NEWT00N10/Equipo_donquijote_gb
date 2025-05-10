from rest_framework import permissions

class IsLibrarianOrAdmin(permissions.BasePermission):
    """
    Permite acciones de escritura solo a usuarios en grupos 'Bibliotecario' o 'Admin'.
    """
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user and request.user.is_authenticated and (
            request.user.groups.filter(name__in=["Bibliotecario", "Admin"]).exists()
        )

class IsOwnerOrStaff(permissions.BasePermission):
    """
    - Métodos de solo lectura: cualquier usuario autenticado.
    - Métodos de escritura (POST/PUT/PATCH/DELETE): sólo Bibliotecario o Admin.
    - A nivel objeto: el mismo usuario o personal.
    """
    def has_permission(self, request, view):
        if request.user and request.user.is_authenticated:
            # Si es staff (Bib/Admin) -> todo
            if request.user.groups.filter(name__in=["Bibliotecario", "Admin"]).exists():
                return True
            # Cliente: permitir SÓLO métodos seguros
            return request.method in permissions.SAFE_METHODS
        return False

    def has_object_permission(self, request, view, obj):
        # Staff accede a todo
        if request.user.groups.filter(name__in=["Bibliotecario", "Admin"]).exists():
            return True
        # Cliente: sólo lo suyo
        return getattr(obj, "borrower_id", None) == request.user.id

