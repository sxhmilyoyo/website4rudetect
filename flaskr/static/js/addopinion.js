$("#test").on('click', function(e) {
  console.log("test18");
    var id  = $(e.target).attr('tweet_id');
    var opinion  = $(e.target).attr('opinion');
    var url = '/addopinion/'+id+'/'+opinion;
    $.get(url);
});
