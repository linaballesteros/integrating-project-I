from django.contrib import admin
from .models import Object  # Import the Object model from your models.py file
from .forms import ObjectForm  # Import the ObjectForm from your forms.py file

class ObjectAdmin(admin.ModelAdmin):
    form = ObjectForm  # Use the custom form for the Object model
    list_display = ('title', 'description', 'brands', 'image', 'date_found', 'place_found', 'hour_range', 'color', 'category', 'place_registered', 'object_status', 'object_recovered')  # Customize displayed fields in the admin list

    def save_model(self, request, obj, form, change):
        print("Enters save model function")
        print("Saving Object in admin")
        super().save_model(request, obj, form, change)

# Register the Object model with the custom admin configuration
admin.site.register(Object, ObjectAdmin)
