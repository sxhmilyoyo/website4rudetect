var requestRunning = false;

$( "#start" ).on( "click", function() {
  if (requestRunning) {
    return;
  }
  // parse font size, if less than 50 increase font size
  console.log("success.");
  $("#start").find("i").removeClass();
  $("#start").find("i").addClass("fa fa-cog fa-spin fa-lg");

  var url = '/process';

  var ajaxOpts = {
    type: 'get',
    url: url,
    success: function(data){
      if (data==="finished") {
        $("#start").find("i").removeClass();
        $("#start").find("i").addClass("fa fa-play");
      }
      // var alert = button_element.parent().siblings('.alert_add').find('.'+data);
      // console.log(alert);
      // alert.stop().fadeTo(500,1).delay(1000).fadeOut(500, function(){requestRunning=false});
    }
  };

  requestRunning = true;
  $.ajax(ajaxOpts);
  return false;
});
