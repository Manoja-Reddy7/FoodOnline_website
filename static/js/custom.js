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

          console.log(latitude);
          console.log(longitude);
            



        }



    });


   
} 