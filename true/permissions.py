from rest_framework.permissions import BasePermission, SAFE_METHODS

def _is_staff_or_superuser(user) -> bool:
    return bool(user and user.is_authenticated and (user.is_staff or user.is_superuser))

class IsStaffOrSuperuserOrReadOnly(BasePermission):
    """
    GET/HEAD/OPTIONS مسموح للجميع.
    أي كتابة/تعديل/حذف → فقط لمستخدم staff أو superuser.
    """
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        return _is_staff_or_superuser(request.user)

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        return _is_staff_or_superuser(request.user)

class IsStaffOrSuperuser(BasePermission):
    """
    كل العمليات (حتى GET) تتطلب staff أو superuser.
    استخدمها للمسارات الإدارية الخالصة (لوحات إدارة/تحليلات).
    """
    def has_permission(self, request, view):
        return _is_staff_or_superuser(request.user)

    def has_object_permission(self, request, view, obj):
        return _is_staff_or_superuser(request.user)

class IsSuperuserOnly(BasePermission):
    """
    حصر الوصول على superuser فقط (لو بدك تشدّها لأقصى درجة).
    """
    def has_permission(self, request, view):
        u = request.user
        return bool(u and u.is_authenticated and u.is_superuser)

    def has_object_permission(self, request, view, obj):
        u = request.user
        return bool(u and u.is_authenticated and u.is_superuser)
