from django.shortcuts import render,get_object_or_404,redirect
from django.contrib.auth.decorators import login_required
from accounts.forms import Userprofileform,UserInfoForm
from accounts.models import UserProfile
from django.contrib import messages


# Create your views here.
@login_required(login_url='login')
def cprofile(request):
    #  Fetch the user's profile or return a 404 if not found
    # Initialize the form with the profile instance to pre-populate with existing data
    profile      = get_object_or_404(UserProfile, user=request.user)
    if request.method == 'POST':
        profile_form  = Userprofileform(request.POST,request.FILES,instance = profile)
        user_form     = UserInfoForm(request.POST,instance=request.user)
        if profile_form.is_valid() and user_form.is_valid():
            profile_form.save()
            user_form.save()
            messages.success(request,'Profile updated')
            return redirect('cprofile')
        else:
            print(user_form.errors)
            print(profile_form.errors)
    else: 
        profile_form = Userprofileform(instance=profile)
        user_form    = UserInfoForm(instance=request.user)
        
    context  = {
       'profile_form' : profile_form,
        'user_form'   : user_form,
        'profile'     : profile
    }
    return render(request,'customers/cprofile.html',context)


    
    