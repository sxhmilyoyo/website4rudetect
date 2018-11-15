$(".opinion").on('click', function(e) {
  console.log($(e.target));
  console.log($(e.target).prop("tagName").toLowerCase())
  console.log($(e.target).attr('stance'));
  if ($(e.target).prop("tagName").toLowerCase() === 'i') {
    console.log('i');
    var button_element = $(e.target).parent();
  } else {
    console.log('button');
    var button_element = $(e.target);
  }
  var content_element = button_element.parent().parent().parent().parent();
  var stance = button_element.attr('stance');
  var tweet_id = content_element.attr('id');
  var url = '/addopinion/'+tweet_id+'/'+stance;
  var dom = `<div class="wrapper alert-inline alert-success alert-dismissible fade show" role="alert" style="display: none">
    submitted successfully!
  </div>`;
  console.log(button_element.parent().parent().siblings('.alert_add'));
  button_element.parent().parent().siblings('.alert_add').append(dom);
  $.get(url, function(data, status){
    // alert("Data: " + $('.alert-inline') + "\nStatus: " + status);
    $('.alert-inline').each(function(i, obj){
      var tweet_id_alert = $(this).parent().parent().parent().attr('id');
      if (tweet_id_alert === tweet_id) {
        // $(this).show(0).delay(1000).hide(0);
        $(this).stop().fadeTo(200,1).delay(1000).fadeOut(200).remove();
      }
    });
  });
});
