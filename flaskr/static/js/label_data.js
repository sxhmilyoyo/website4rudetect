var requestRunning = false;

$(".tsbtn").on('click', function(e) {
  if (requestRunning) {
    // console.log("requestRunning...");
    return;
  }
  // console.log($(e.target));
  // console.log($(e.target).prop("tagName").toLowerCase())
  // console.log($(e.target).attr('stance'));
  // console.log('button');
  var button_element = $(e.target);
  var content_element = button_element.parent().parent().siblings('a');
  console.log(content_element);
  var stance = button_element.attr('stance');
  console.log(stance);
  var tweet_id = content_element.attr('id');
  console.log(tweet_id);
  var url = '/addopinion/'+tweet_id+'/'+stance;

  // $.get(url, function(data, status){
  //   var alert = button_element.parent().parent().siblings('.alert_add').find('.'+data);
  //   console.log(alert);
  //   alert.stop().fadeTo(500,1).delay(1000).fadeOut(500);
  // });

  var ajaxOpts = {
    type: 'get',
    url: url,
    success: function(data){
      var alert = button_element.parent().siblings('.alert_add').find('.'+data);
      // console.log(alert);
      alert.stop().fadeTo(500,1).delay(1000).fadeOut(500, function(){requestRunning=false});
    }
  };

  requestRunning = true;
  $.ajax(ajaxOpts);
  return false;
});