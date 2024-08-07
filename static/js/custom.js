let autocomplete;

function initAutoComplete(){
autocomplete = new google.maps.places.Autocomplete(
    document.getElementById('id_address'),
    {
        types: ['geocode', 'establishment'],
        //default in this app is "IN" - add your country code
        componentRestrictions: {'country': ['in']},
    })
// function to specify what should happen when the prediction is clicked
autocomplete.addListener('place_changed', onPlaceChanged);
}

function onPlaceChanged (){
    var place = autocomplete.getPlace();

  

    // User did not select the prediction. Reset the input field or alert()
    if (!place.geometry){
        document.getElementById('id_address').placeholder = "Start typing...";
    }
    else{
        //console.log('place name=>',place)
    }
    // get the address components and assign them to the fields

    var geocoder = new google.maps.Geocoder()
    var address  = document.getElementById('id_address').value

    geocoder.geocode({'address': address}, function(results,status){
    
        if (status == google.maps.GeocoderStatus.OK){

            var latitude = results[0].geometry.location.lat();
            var longitude = results[0].geometry.location.lng();

            $('#id_lattitude').val(latitude);
            $('#id_langitude').val(longitude);
            $('#id_address').val(address);
        }

    });


   // Loop through the address components and other address data.
   console.log(place.address_components)

   for(var i=0; i<place.address_components.length;i++)
   {
    for(var j=0;j<place.address_components[i].types.length;j++){
        // get country
        if (place.address_components[i].types[j]=='country'){
            $('#id_country').val(place.address_components[i].long_name);
        }
         // get state
        if (place.address_components[i].types[j]=='administrative_area_level_1'){
            $('#id_state').val(place.address_components[i].long_name);
        }
         // get city
        if (place.address_components[i].types[j]=='locality'){
            $('#id_city').val(place.address_components[i].long_name);
        }
        if (place.address_components[i].types[j]=='postal_code'){
            $('#id_pin_code').val(place.address_components[i].long_name);
        }else{
            $('#id_pin_code').val('')
        }

    }
   }
} 
$(document).ready(function(){
    // Add to cart.
    $('.add_to_cart').on('click',function(e){
        e.preventDefault();
        food_id = $(this).attr('data-id');
         url     = $(this).attr('data-url');
        $.ajax({
            type    : 'GET',
            url     : url,
            success  : function(response){
                console.log(response)
                if (response.status == 'Login Required')
                {
                    swal(response.message, '', 'info').then(function() {
                        window.location = '/login' // Redirect to the login page
                    })
                }else if (response.status == 'Failed'){
                        swal(response.message, '', 'error')
                }else{
                    $('#cart-counter').html(response.cart_counter['cart_count'])
                    $('#qty-' +food_id).html(response.qty)
                    applyCartAmounts(
                        response.cart_amount['subtotal'],
                        response.cart_amount['grand_total'],
                        response.cart_amount['tax']
                    )

                } 
            }
        });

    });
   

    // Place the cart item quantity on load.
    $('.item-qty').each(function(){
        var the_id = $(this).attr('id')
        var qty = $(this).attr('data-qty')
        console.log(qty)
        $('#'+the_id).html(qty)
    });
    //Decrease cart.

    $('.decrease_cart').on('click',function(e){
        e.preventDefault();
        food_id = $(this).attr('data-id');
        url     = $(this).attr('data-url');
        cart_id = $(this).attr('id')
        
        $.ajax({
            type    : 'GET',
            url     : url,
            success  : function(response){
                console.log(response)
                if (response.status == 'Login Required')
                {
                    swal(response.message, '', 'info').then(function() {
                        window.location = '/login' // Redirect to the login page
                    })
                }else if (response.status == 'Failed'){
                        swal(response.message, '', 'error')
                }else{
                    $('#cart-counter').html(response.cart_counter['cart_count'])
                    $('#qty-' +food_id).html(response.qty)
                    if (window.location.pathname == '/marketplace/cart/'){
                        removeCartItem(response.qty,cart_id);
                        CheckEmptycart();
                    
    
                    } 
                    applyCartAmounts(
                        response.cart_amount['subtotal'],
                        response.cart_amount['grand_total'],
                        response.cart_amount['tax']
                    )
                } 
            }
               
        });

    });

    //Delete Cart

    $('.delete_cart').on('click',function(e){
        e.preventDefault();
        cart_id = $(this).attr('data-id');
         url     = $(this).attr('data-url');
        $.ajax({
            type    : 'GET',
            url     : url,
            success  : function(response){
                //log in not required beacause i already added the log in required decorator in view
                 if (response.status == 'Failed'){
                        swal(response.message, '', 'error')
                }else{
                    $('#cart-counter').html(response.cart_counter['cart_count'])
                    swal(response.status,response.message,'success');
                        removeCartItem(0,cart_id)
                        CheckEmptycart();
                
            }
            applyCartAmounts(
                response.cart_amount['subtotal'],
                response.cart_amount['grand_total'],
                response.cart_amount['tax']
            )
            }
        });

    });
    // Delete the cart item if the quantity is 0.
    function removeCartItem(cartItemQty,cart_id) {
        if(cartItemQty<= 0){

            // Remove the cart item.
            document.getElementById("cart-item-"+cart_id).remove()
        }
    }
    // check cart is empty or not.
    function CheckEmptycart(){
        var cart_counter = document.getElementById('cart-counter').innerHTML
        if (cart_counter == 0){
            document.getElementById('empty_cart').style.display = 'block';
        }
    

    }
    // get cart amount.
    function applyCartAmounts(subtotal,grand_total,tax){
        if (window.location.pathname == '/marketplace/cart/'){
            $('#subtotal').html(subtotal)
            $('#total').html(grand_total)
            $('#tax').html(tax)

        }

    }
    
});
    





