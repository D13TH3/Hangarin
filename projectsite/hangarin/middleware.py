from django.shortcuts import redirect
from django.conf import settings


class LoginRequiredMiddleware:
    """Redirect unauthenticated users to the login page when accessing protected URLs."""
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if not request.user.is_authenticated:
            path = request.path.lstrip("/")
            allowed_prefixes = (
                "admin/",
                "accounts/",  # allauth: login, signup, social
                "static/",
                "favicon.ico",
            )
            if path == "" or not any(path.startswith(p) for p in allowed_prefixes):
                return redirect(settings.LOGIN_URL + "?next=" + request.get_full_path())
        return self.get_response(request)
