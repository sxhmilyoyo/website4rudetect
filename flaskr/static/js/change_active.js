$( "nav .nav-link" ).on( "click", function() {
  // parse font size, if less than 50 increase font size
  console.log("success.");
  $(".nav").find(".active").removeClass("active");
  $( this ).parent().addClass("active");
});
