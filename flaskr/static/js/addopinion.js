var requestRunning = false;

$(".opinion").on('click', function(e) {
  if (requestRunning) {
    console.log("requestRunning...");
    return;
  }
  console.log($(e.target));
  // console.log($(e.target).prop("tagName").toLowerCase())
  // console.log($(e.target).attr('stance'));
  if ($(e.target).prop("tagName").toLowerCase() === 'i') {
    console.log('i');
    var button_element = $(e.target).parent();
  } else {
    console.log('button');
    var button_element = $(e.target);
  }
  var content_element = button_element.parent().parent().parent().parent();
  var stance = button_element.attr('stance');
  var flag = button_element.attr('flag');  
  var tweet_id = content_element.attr('id');

  console.log(stance);
  console.log(flag);
  console.log(tweet_id);

  var url = '/addopinion/'+tweet_id+'/'+flag+'/'+stance;

  // $.get(url, function(data, status){
  //   var alert = button_element.parent().parent().siblings('.alert_add').find('.'+data);
  //   console.log(alert);
  //   alert.stop().fadeTo(500,1).delay(1000).fadeOut(500);
  // });

  var ajaxOpts = {
    type: 'get',
    url: url,
    success: function(data){
      var alert = button_element.parent().parent().siblings('.alert_add').find('.'+data);
      console.log(alert);
      alert.stop().fadeTo(500,1).delay(1000).fadeOut(500, function(){requestRunning=false});
    }
  };

  requestRunning = true;
  $.ajax(ajaxOpts);
  return false;
});
