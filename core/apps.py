from django.apps import AppConfig
import os

#class CoreConfig(AppConfig):
    #name = 'core'

class CoreConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "core"
    path = os.path.dirname(os.path.abspath(__file__))  # ✅ FIX


#/////////Auto old File Delete Code when new file replaced///