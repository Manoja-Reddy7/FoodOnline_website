from django.shortcuts import render,redirect
from .forms import UserForm
from .models import User
from django.contrib import messages

# Create your views here.

def registerUser(request):
    
    '''In the context of web forms, 
    POST requests are used when submitting data to the server, such as when a user submits a form.'''
    if request.method=='POST':
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
            messages.error(request,'Your account has been registered successfully!')
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
       
    
    