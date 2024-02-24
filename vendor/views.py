from django.shortcuts import get_object_or_404, render, redirect
from .forms import VendorForm
from accounts.forms import Userprofileform
from accounts.models import UserProfile
from .models import Vendor
from django.contrib import messages
from django.contrib.auth.decorators import login_required,user_passes_test
from accounts.views import check_role_vendor

@login_required(login_url='login')   
@user_passes_test(check_role_vendor)
def vprofile(request):
    profile = get_object_or_404(UserProfile, user=request.user) 
    vendor = get_object_or_404(Vendor, user=request.user)
    
    context = {
        'vendor_form': None,
        'profile_form': None,
        'vendor': vendor,
        'profile': profile,
    }

    if request.method == "POST":
        profile_form = Userprofileform(request.POST, request.FILES, instance=profile) 
        vendor_form = VendorForm(request.POST, request.FILES, instance=vendor)

        if profile_form.is_valid() and vendor_form.is_valid():
            profile_form.save()
            vendor_form.save()
            messages.success(request, "Your settings updated.")
            return redirect('vprofile')
        else:
            print(profile_form.errors)
            print(vendor_form.errors)
            context['profile_form'] = profile_form
            context['vendor_form'] = vendor_form

    else:
        context['profile_form'] = Userprofileform(instance=profile)
        context['vendor_form'] = VendorForm(instance=vendor)

    return render(request, 'vendor/vprofile.html', context)
