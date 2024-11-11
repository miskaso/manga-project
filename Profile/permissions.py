from rest_framework.permissions import BasePermission


# Здесь настроим роли пользователям
class HasRolePermission(BasePermission):
    def has_permission(self, request, view):
        required_role = view.kwargs.get('role')
        if required_role:
            user_roles = request.user.userrole_set.all()
            return any(role.role.name == required_role for role in user_roles)
        return False
