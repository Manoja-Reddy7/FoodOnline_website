from django.http import HttpResponse
from django.shortcuts import render

from vendor.models import Vendor

'''def home(request):
    vendors  = Vendor.objects.filter(is_approved = True, user__is_active =  True)[:8]
    print(vendors)
    
    context = {
        'vendors': vendors,
        
    }
    return render(request,'home.html',context)'''
  
def home(request):
    # Retrieve a specific vendor or set of vendors based on criteria
    vendor = Vendor.objects.filter(is_approved=True, user__is_active=True).first()  # Example: Retrieve the first vendor

    context = {
        'vendor': vendor,  # Assign the retrieved vendor to the 'vendor' variable in the context
        # Other context variables...
    }

    return render(request, 'home.html', context)
