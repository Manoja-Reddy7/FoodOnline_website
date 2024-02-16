from django.shortcuts import render,redirect
from vendor.forms import VendorForm
from .forms import UserForm
from .models import User,UserProfile
from django.contrib import messages,auth
from .utils import detectUser
from django.contrib.auth.decorators import login_required,user_passes_test
from django.core.exceptions import PermissionDenied

# Restrict the Vendor from customer page

def check_role_vendor(user):
    if user.role==1:
        return True
    else:
        raise PermissionDenied

# Restrict the customer  from Vendor page

def check_role_customer(user):
    if user.role==2:
        return True
    else:
        raise PermissionDenied


def registerUser(request):
     if request.user.is_authenticated:
        messages.warning(request,'You are already logged in!')
        return redirect('myAccount')
    
        '''In the context of web forms, 
        POST requests are used when submitting data to the server, such as when a user submits a form.'''
     elif request.method=='POST':
        # request.POST prints the contents of the request.POST dictionary to the console.
        # form = UserForm(request.POST),it creates an instance of the UserForm using the data from request.POST
        # This condition checks if the submitted form data is valid according to the rules defined in the UserForm class.
         print(request.POST)
         form = UserForm(request.POST)
         if form.is_valid():
            # the form is ready to save, this is not yet save.
            # After we submit the form the data with fields is stored in the cleaned_data dictionary.
            password = form.cleaned_data['password']
            user = form.save(commit=False)
            user.role = User.CUSTOMER
            user.set_password(password)
            user.save()
            messages.success(request,'Your account has been registered successfully!')
            return redirect('registerUser')
         else:
            print(form.errors)
            print("Invalid Form.")
     else:
        # When user first visit and enter the webpage url the form will display on the webpage i.e GET request.
        # calling the Userform class 
        form = UserForm()
        context = {
         'form':form,
             }
        return render(request, 'accounts/registerUser.html',context)

def registerVendor(request):
    userform = UserForm()
    v_form  = VendorForm()
    context = {
            'form'  : userform,
            'v_form': v_form,
           }
    if request.user.is_authenticated:
        messages.warning(request,'You are already logged in!')
        return redirect('myAccount')
    
    elif request.method=='POST':
        # store the data and create user
        form = UserForm(request.POST)
        v_form = VendorForm(request.POST,request.FILES)
        if form.is_valid() and v_form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name  = form.cleaned_data['last_name']
            email      = form.cleaned_data['email']
            username   = form.cleaned_data['username']
            password   = form.cleaned_data['password']
            user       =  User.objects.create_user(first_name=first_name,last_name=last_name,email=email,username=username,password=password)
            user.role = User.VENDOR
            user.save()
            vendor = v_form.save(commit=False)
            vendor.user = user
            user_profile = UserProfile.objects.get(user=user)
            vendor.user_profile = user_profile
            vendor.save()
            messages.success(request,"Your account has been registered sucessfully! Please wait for the approval.")
            return redirect('registerVendor')
        else:
            print(form.errors)
            print(v_form.errors)
            print("Invalid form")
    else:
        '''userform = UserForm()
        v_form  = VendorForm()
        context = {
            'form'  : userform,
            'v_form': v_form,
           }'''
    return render(request,'accounts/registerVendor.html',context)

def login(request):
    if request.user.is_authenticated:
        messages.warning(request,'You are already logged in!')
        return redirect('myAccount')
        
        
    elif request.method =="POST":
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = auth.authenticate(email=email,password=password)
        
        if user is not None and user.is_active:
            auth.login(request,user)
            messages.success(request, 'You are logged in.')
            return redirect('myAccount')
        else:
            messages.error(request,'Invalid log in credentials')
            return redirect('login')
            
    return render(request,'accounts/login.html')

def logout(request):
    auth.logout(request)
    messages.info(request,'You are logged out.')
    return redirect('login')


# When you logged into the account then only you have access to the myaccount dashboard.

@login_required(login_url='login')
def myAccount(request):
    user = request.user
    print(user)
    redirecturl = detectUser(user)
    return redirect(redirecturl)

@login_required(login_url='login')   
@user_passes_test(check_role_customer)
def custDashboard(request):
    return render (request,'accounts/custDashboard.html')


@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def vendorDashboard(request):
    return render (request,'accounts/vendorDashboard.html')



    
    
       
    
    
    
        