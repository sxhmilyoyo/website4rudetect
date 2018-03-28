$( "#p" ).on( "click", function() {
  // parse font size, if less than 50 increase font size
  $( this ).removeClass("nav-small").addClass("nav-big");
  $( "#c" ).removeClass("nav-big").addClass("nav-small");
});

$( "#c" ).on( "click", function() {
  // parse font size, if less than 50 increase font size
  $( this ).removeClass("nav-small").addClass("nav-big");
  $( "#p" ).removeClass("nav-big").addClass("nav-small");
});
