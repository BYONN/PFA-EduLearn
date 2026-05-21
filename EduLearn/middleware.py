from django.shortcuts import render
from users.models import PlatformSetting

class MaintenanceModeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Exclude administrative views, login, logout, static files, and media from maintenance check
        if (request.path.startswith('/admin') or 
            request.path.startswith('/admin-panel') or 
            request.path.startswith('/login') or 
            request.path.startswith('/logout') or 
            request.path.startswith('/static/') or 
            request.path.startswith('/media/')):
            return self.get_response(request)
            
        settings = PlatformSetting.get_settings()
        if settings.maintenance_mode and not request.user.is_superuser:
            # Render a custom beautiful maintenance page
            return render(request, 'maintenance.html', status=503)
            
        return self.get_response(request)
