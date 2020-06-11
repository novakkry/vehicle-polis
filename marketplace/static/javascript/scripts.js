$(document).ready(function() {
 // executes when HTML-Document is loaded and DOM is ready
console.log("document is ready");
  

  $( ".card" ).hover(
  function() {
    $(this).addClass('shadow-lg').css('cursor', 'pointer'); 
  }, function() {
    $(this).removeClass('shadow-lg');
  }
);
  
// document ready  
});

function myMap() {
var mapProp= {
  center:new google.maps.LatLng(-27.483880,153.011527),
  zoom:8,
        panControl: false,
      zoomControl: true,
      scaleControl: false,
      streetViewControl: false,
      mapTypeControl: false

};
var map = new google.maps.Map(document.getElementById("googleMap"),mapProp);
}

// Rating Initialization
$(document).ready(function() {
  $('#rateMe2').mdbRate();
});