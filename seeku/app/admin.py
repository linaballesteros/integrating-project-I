from django.contrib import admin
from .models import Object, Noti,Claim_Complaint,Search,HistorySearches
from .forms import ObjectForm, ClaimObject, ClaimComplaint
class ObjectAdmin(admin.ModelAdmin):
    form = ObjectForm  # Use the custom form for the Object model
    list_display = ('title', 'description', 'brands', 'image', 'date_found', 'place_found', 'hour_range', 'color', 'category', 'place_registered', 'object_status', 'object_recovered')  # Customize displayed fields in the admin list
    search_fields=['id','title']
    def save_model(self, request, obj, form, change):
        print("Enters save model function")
        print("Saving Object in admin")
        super().save_model(request, obj, form, change)

# Register the Object model with the custom admin configuration
admin.site.register(Object)#, ObjectAdmin)
admin.site.register(Noti)
admin.site.register(Claim_Complaint)
admin.site.register(Search)
admin.site.register(HistorySearches)