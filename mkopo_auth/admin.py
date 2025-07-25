from django.contrib import admin

# Register your models here.


# Register your models here.
from django.apps import apps
from django.contrib import admin

from .models import *

# Get the AppConfig for the 'auth_app' app
app_config = apps.get_app_config("mkopo_auth")

# Get all models in the app
models = app_config.get_models()

# Register all models in the admin site
for model in models:
    # Create a list of all field names in the model
    field_names = [field.name for field in model._meta.fields]
    search_field_names = [field.name for field in model._meta.fields]

    # If the model has a foreign key field, exclude the related field from the search fields
    for field in model._meta.fields:
        if field.related_model:
            related_field_name = f"{field.name}"
            if related_field_name in search_field_names:
                search_field_names.remove(related_field_name)

    # Register the model with all fields displayed and filters enabled
    admin.site.register(
        model,
        list_display=field_names,
        list_filter=field_names,
        search_fields=search_field_names,
        list_per_page=9,


    )