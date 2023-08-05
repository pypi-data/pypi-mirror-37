
import sys
from django.apps import apps
from django.apps.registry import Apps


_settings = sys.modules['django.conf'].settings

if 'core' in getattr(_settings, 'INSTALLED_APPS'):
    setattr(_settings, 'EMAIL_USE_TLS', True)
    setattr(_settings, 'DEFAULT_FROM_EMAIL', 'email de envio')
    setattr(_settings, 'EMAIL_HOST', 'host de email')
    setattr(_settings, 'EMAIL_HOST_USER', '')
    setattr(_settings, 'EMAIL_HOST_PASSWORD', '')
    setattr(_settings, 'EMAIL_PORT', 25) 
    setattr(_settings, 'LOGIN_REDIRECT_URL', '/core/')
    setattr(_settings, 'LOGIN_URL', '/core/login/')
    setattr(_settings, 'LOGOUT_REDIRECT_URL', '/core/login/')
