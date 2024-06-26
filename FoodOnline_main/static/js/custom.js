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
        var food_id = $(this).attr('data-id');
        var url     = $(this).attr('data-url');
        console.log(food_id,url)
        var data={
            food_id : food_id,
        }
        $.ajax({
            type    : 'GET',
            url     : url,
            data : data,
            success  : function(response){
                console.log("AJAX response:", response); 
                if (response.status == 'Login_required'){
                    swal(response.message,'','info').then(function(){
                        window.location = '/login';  // Redirect to the login page
                    })
                }else if(response.status == 'Failed'){
                    swal(response.error,'','error')
                }else{
               $('#qty-'+food_id).html(response.qty);
               $('#cart-counter').html(response.cart_counter['cart_count']);

               // subtotal, tax and grand total.
          applyCartAmounts(response.cart_amount['subtotal'],
                           response.cart_amount['grand_total'],
                           response.cart_amount['tax_dict'],
                         )

               }
            }
        });

    });
   

    // Place the cart item quantity on load.
    $('.item-qty').each(function(){
        var the_id = $(this).attr('id')
        var qty = $(this).attr('data-qty')
        // placing the item quantity for individual items.
        $('#'+the_id).html(qty)
    });
    //Decrease cart.

    $('.decrease_cart').on('click',function(e){
        e.preventDefault();
        food_id = $(this).attr('data-id');
        url     = $(this).attr('data-url');
        cart_id = $(this).attr('id');

        $.ajax({
            type    : 'GET',
            url     : url,
            success  : function(response){
       
                if (response.status == 'Login_required'){
                    swal(response.message,'','info').then(function(){
                        window.location = '/login';  // Redirect to the login page
                    })
                }else if(response.status == 'Failed'){
                    swal(response.message,'','error')
                }else{
               $('#qty-'+food_id).html(response.qty);
               $('#cart-counter').html(response.cart_counter['cart_count']);

               applyCartAmounts(response.cart_amount['subtotal'],
               response.cart_amount['grand_total'],
               response.cart_amount['tax_dict'],

 
                 )
               console.log(response.cart_counter['cart_count']);
               if(window.location.pathname == '/marketplace/cart/'){  
                
                        removeCartItem(response.qty,cart_id)
                        CheckEmptycart()
                        } 
            }
        }
               
        });

    });

    //Delete Cart

    $('.delete_cart').on('click',function(e){
        e.preventDefault();
        

        cart_id = $(this).attr('data-id');
        url     = $(this).attr('data-url');
        console.log(cart_id);
     
        
        $.ajax({
            type    : 'GET',
            url     : url,
            success  : function(response){
                console.log(response);
               if(response.status == 'Failed'){
                    swal(response.message,'','error')
                }else{
               $('#cart-counter').html(response.cart_counter['cart_count']);
               swal(response.status,response.message,'success');

               applyCartAmounts(response.cart_amount['subtotal'],
                                response.cart_amount['grand_total'],
                                response.cart_amount['tax_dict'],
                               );
               removeCartItem(0,cart_id)
               CheckEmptycart()

               }
               
            }
               
        });
        
    });
    function removeCartItem(cartItemQty,cart_id) {
        
        console.log(cart_id)
   
        if(cartItemQty<= 0){
            // Remove the cart item.
            document.getElementById("cart-item-"+cart_id).remove()
           }

    }
    // Delete the cart item if the quantity is 0.
    
    // check cart is empty or not.
    function CheckEmptycart(){
        var cart_counter = document.getElementById('cart-counter').innerHTML
        if (cart_counter == 0){
            document.getElementById('empty_cart').style.display = 'block';
        }
    

    }
    // get cart amount.
   function applyCartAmounts(subtotal,grand_total,tax_dict){
        if (window.location.pathname == '/marketplace/cart/'){
            // setting the subtotal,total and tax amounts in cart page.
            $('#subtotal').html(subtotal)
            $('#total').html(grand_total)
            console.log(tax_dict)
            for(key1 in tax_dict){
                console.log(tax_dict[key1])
                for(key2 in tax_dict[key1]){
                    console.log(tax_dict[key1][key2])
                    $('#tax-'+key1).html(tax_dict[key1][key2])

                }
            }

        }

    }
    //Add opening hour
    $('.add-hour').on('click',function(e) {
       var day       = document.getElementById('id_day').value
       var from_hour = document.getElementById('id_from_hour').value
       var to_hour   = document.getElementById('id_to_hour').value
       var is_closed = document.getElementById('id_is_closed').checked
       var csrftoken = $('input[name=csrfmiddlewaretoken]').val()
       var url       = document.getElementById('add_hour_url').value
       
       if(is_closed){
        is_closed = 'True'
        condition = "day!=''"
       }else{
        is_closed = 'False'
        condition = "day!='' && from_hour!='' && to_hour!=''"
       }


       if (eval(condition))
        {
           $.ajax({
            type : 'POST',
            url  :  url,
            data :{
                'day': day,
                'from_hour':from_hour,
                'to_hour':to_hour,
                'is_closed': is_closed,
                'csrfmiddlewaretoken':csrftoken,
                },
                success:function(response){ 
                    if(response.status == 'success'){
                        if(response.is_closed == 'Closed'){
                            html  = '<tr id="hour-'+response.id+'"><td><b>'+response.day+'</b></td><td>Closed</td><td><a href="#" class="remove_hour" data-url="/vendor/opening-hours/remove/'+response.id+'">Remove</a></td></tr>'
                        }else{
                            html  = '<tr id="hour-'+response.id+'"><td><b>'+response.day+'</b></td><td>'+response.from_hour+' - '+response.to_hour+'</td><td><a href="#" class="remove_hour" data-url="/vendor/opening-hours/remove/'+response.id+'">Remove</a></td></tr>'                        
                        }
                    $(".opening_hours").append(html)
                    document.getElementById("opening_hours").reset();
                    }else{
                        console.log(response.error)
                        swal(response.message, '',"error")
                    }
                }
           });
        }else{
            swal("Please fill all the fields.",'','info')
        }
    });
    //Remove opening hour.
    $(document).on('click','.remove_hour',function(e){
        e.preventDefault();
        url = $(this).attr('data-url');
        console.log(url)
        $.ajax({
            type    : 'GET',
            url     : url,
            success : function(response){
                if(response.status == "success"){
                    document.getElementById('hour-'+response.id).remove()
                }
                console.log(response)


            }
        })

    });
    
// document ready close

});