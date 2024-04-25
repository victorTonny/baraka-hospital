from django.http import HttpResponseForbidden

def doctor_required(view_func):
    def _wrapped_view(request, *args, **kwargs):
        if request.user.is_authenticated and hasattr(request.user, 'specialist') and request.user.specialist.area_of_specialist == 'Doctor':
            return view_func(request, *args, **kwargs)
        else:
            # Handle unauthorized access
            return HttpResponseForbidden("You don't have permission to access this page.")
    return _wrapped_view


def receptionist_required(view_func):
    def _wrapped_view(request, *args, **kwargs):
        if request.user.is_authenticated and request.user.specialist.area_of_specialist == 'Receptionist':
            return view_func(request, *args, **kwargs)
        else:
            # Handle unauthorized access
            return HttpResponseForbidden("You don't have permission to access this page.")
    return _wrapped_view

def admin_required(view_func):
    def _wrapped_view(request, *args, **kwargs):
        if request.user.is_authenticated and request.user.is_staff:
            return view_func(request, *args, **kwargs)
        else:
            # Handle unauthorized access
            return HttpResponseForbidden("You don't have permission to access this page.")
    return _wrapped_view
