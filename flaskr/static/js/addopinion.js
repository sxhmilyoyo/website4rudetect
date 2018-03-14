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
  var content_element = button_element.parent().parent();
  var stance = button_element.attr('stance');
  var tweet_id = content_element.attr('id');
  var url = '/addopinion/'+tweet_id+'/'+stance;
  $.get(url);
});
