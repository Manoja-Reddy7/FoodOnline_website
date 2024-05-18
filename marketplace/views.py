from django.shortcuts import render
from vendor.models import Vendor
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect

from menu.models import Category,FoodItem
from .models import Cart

from django.db.models import Prefetch,Q
from django.http import HttpResponse,JsonResponse

from.context_processors import get_cart_counter,get_cart_amounts
from django.contrib.auth.decorators import login_required

from django.contrib.gis.geos import GEOSGeometry
from django.contrib.gis.measure import Distance as D  # ``D`` is a shortcut for distance

from django.contrib.gis.db.models.functions import Distance

# Create your views here.
def marketplace(request):
    # listings.html will holds the list of vendors.
    vendors         = Vendor.objects.filter(is_approved = True, user__is_active =  True)
    vendor_count    = vendors.count()
    context  = {
        'vendors'       : vendors,
        'vendor_count'  : vendor_count,
        
    }
    return render(request, 'marketplace/listings.html',context) 

def vendor_detail(request,vendor_slug): 
    
    vendor      = get_object_or_404(Vendor,vendor_slug=vendor_slug)
    categories    = Category.objects.filter(vendor=vendor).prefetch_related(
        Prefetch(
            'fooditems',
            queryset= FoodItem.objects.filter(is_available=True)
        )
    )
    if request.user.is_authenticated:
        cart_items  = Cart.objects.filter(user=request.user)
        
    else:
        cart_items  = None
    
    context = {
        'vendor'   : vendor,
        'categories' : categories,
        'cart_items' : cart_items,
    }
    
    return render(request,'marketplace/vendor_detail.html',context)



def add_to_cart(request, food_id):
    # Check if the user is authenticated
    if request.user.is_authenticated:
        # Check if the request method is GET and has the 'HTTP_X_REQUESTED_WITH' header set to 'XMLHttpRequest'
        if request.method == 'GET' and request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
            try:
                # Get the food item
                fooditem = get_object_or_404(FoodItem, id=food_id)
                
                # Check if the user has already added the food item to the cart
                checkcart, created = Cart.objects.get_or_create(user=request.user, fooditem=fooditem, defaults={'quantity': 1})
                
                # If cart is already exit then we need to increase the cart.
                if not created:
                    # Increase the cart quantity
                    checkcart.quantity += 1
                    checkcart.save()
                    return JsonResponse({'status': 'Success', 'message': 'Increased the cart quantity.', 'cart_counter': get_cart_counter(request), 'qty': checkcart.quantity,'cart_amount' : get_cart_amounts(request)})
                else:
                    return JsonResponse({'status': 'Success', 'message': 'Item added to cart.','cart_counter': get_cart_counter(request), 'qty': checkcart.quantity,'cart_amount' : get_cart_amounts(request)})
            except FoodItem.DoesNotExist:
                return JsonResponse({'status': 'Failed', 'message': 'The food item does not exist!'})
        else:
            # Return a 400 Bad Request response if the request is not AJAX
            return JsonResponse({'error': 'Invalid request'}, status=400)
    else:
        # Return a 401 Unauthorized response if the user is not authenticated
        return JsonResponse({'status': 'Login Required', 'message': 'Please log in to continue!'})
def decrease_cart(request,food_id):
    
     # Check if the user is authenticated
    if request.user.is_authenticated:
        if request.method == 'GET' and request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
            # Check if the food item exist.
            
            try:
                fooditem  = FoodItem.objects.get(id=food_id)
                # check if the item is already added in the cart.
                try:
                    checkcart = Cart.objects.get(user=request.user,fooditem=fooditem)
                    if checkcart.quantity > 1:
                        checkcart.quantity -= 1
                        checkcart.save()
                    else:
                        checkcart.delete()
                        checkcart.quantity = 0 
                    return JsonResponse({'status': 'Success', 'cart_counter': get_cart_counter(request), 'qty': checkcart.quantity,'cart_amount' : get_cart_amounts(request)})     
                except:
                     return JsonResponse({'status': 'Failed', 'message': 'You dont have this item in cart!'})     
            except:
               return JsonResponse({'status': 'Failed', 'message': 'Food item Doesnot exist.'})     
        else:
            # Return a 400 Bad Request response if the request is not AJAX
            return JsonResponse({'error': 'Invalid request'}, status=400)
    else:
        return JsonResponse({'status': 'Login Required', 'message': 'Please log in to continue!'})

@login_required(login_url='login')
def cart(request):
    cart_items = Cart.objects.filter(user=request.user)
    context = {
        'cart_items' : cart_items,
    }
    return render(request,'marketplace/cart.html',context) 


def delete_cart(request,cart_id):
    if request.user.is_authenticated:
         if request.method == 'GET' and request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
              try:
                cart_item = Cart.objects.get(user=request.user,id=cart_id)
                if cart_item:
                    cart_item.delete()
                    return JsonResponse({'status': 'Success','message':'Cart item has been deleted.','cart_counter': get_cart_counter(request),'cart_amount' : get_cart_amounts(request)})
              except:
                    return JsonResponse({'status': 'Failed', 'message': 'Cart item Doesnot exist.'})   
         else: 
            JsonResponse({'error': 'Invalid request'}, status=400)
def search(request):
    print(request.GET)
    if 'address' not in request.GET:
        # Redirect to marketplace if 'address' parameter is missing
        return redirect('marketplace')  
    else:
        address = request.GET['address']
        latitude = request.GET['lat']
        longitude = request.GET['lan']
        radius = request.GET['radius']
        keyword = request.GET['keyword']
        # Query to fetch vendors based on food items or vendor name keyword
        fetch_vendors_by_food_items = FoodItem.objects.filter(food_title__icontains=keyword, is_available=True).values_list('vendor', flat=True)
        vendors = Vendor.objects.filter(
                    Q(id__in=fetch_vendors_by_food_items) |
                    Q(vendor_name__icontains=keyword, is_approved=True, user__is_active=True)
                )

        # Apply location-based filtering and distance annotation
        pnt = GEOSGeometry('POINT(%s %s)' % (longitude, latitude))
        vendors = Vendor.objects.filter(user_profile__location__distance_lte=(pnt, D(km=400))).annotate(distance=Distance('user_profile__location', pnt)).order_by("distance")
        

        # Add 'kms' attribute to each vendor for distance in kilometers
        for v in vendors:
            v.kms = round(v.distance.km, 1)

        vendor_count = vendors.count()
        context = { 
                    'vendors': vendors,
                    'vendor_count': vendor_count,
                    'source_location': address,
                }
        return render(request, 'marketplace/listings.html', context)
            
