$('#nav-tab #nav-chart-tab').on('shown.bs.tab', function (e) {
// $('a[data-toggle="tab"]').on('show.bs.tab', function (e) {
  console.log("test");
  var num_support_tweets = $("#listSupportOriginTweets").attr('class');
  var num_oppose_tweets = $("#listOpposeOriginTweets").attr('class');
  var num_support_snippets = $("#listSupportOriginSnippet").attr('class');
  var num_oppose_snippets = $("#listOpposeOriginSnippet").attr('class');
  var ctx_tweet = $("#myChartTweet");
  var ctx_snippet = $("#myChartSnippet");
  
  var data_tweet = {
    datasets: [{
        label: "Percentage of Stance for Tweets",
        data: [parseInt(num_support_tweets), parseInt(num_oppose_tweets)],
        // data2: [parseInt(num_support_snippets), parseInt(num_oppose_snippets)],        
        backgroundColor: [
                'rgb(255, 99, 132)',
                'rgb(255, 205, 86)'
            ],
        borderWidth: 3
    }],
    // These labels appear in the legend and in the tooltips when hovering different arcs
    labels: [
        'SUPPORT',
        'OPPOSE'
    ]
  };

  var data_snippet = {
    datasets: [{
        label: "Percentage of Stance for News",
        // data: [parseInt(num_support_tweets), parseInt(num_oppose_tweets)],
        data: [parseInt(num_support_snippets), parseInt(num_oppose_snippets)],        
        backgroundColor: [
                'rgb(255, 99, 132)',
                'rgb(255, 205, 86)'
            ],
        borderWidth: 3
    }],
    // These labels appear in the legend and in the tooltips when hovering different arcs
    labels: [
        'SUPPORT',
        'OPPOSE'
    ]
  };

  var options_Tweet = {
    responsive: false,
    animation: {
      animateRotate: true
    },
    layout: {
            padding: {
                left: 0,
                right: 0,
                top: 0,
                bottom: 10
            }
    },
    title: {
            display: true,
            text: 'Percentage of Stance for Tweets',
            padding: 20,
            fontSize: 20,
            lineHeight: 2.0
    },
    legend: {
            display: true,
            position: 'top',
            fullWidth: true
    }
  };

  var options_Snippet = {
    responsive: false,
    animation: {
      animateRotate: true
    },
    layout: {
            padding: {
                left: 0,
                right: 0,
                top: 0,
                bottom: 10
            }
    },
    title: {
            display: true,
            text: 'Percentage of Stance for News',
            padding: 20,
            fontSize: 20,
            lineHeight: 2.0
    },
    legend: {
            display: true,
            position: 'top',
            fullWidth: true
    }
  };

  var myPieChartTweet = new Chart(ctx_tweet,{
    type: 'pie',
    data: data_tweet,
    options: options_Tweet
  });

  var myPieChartSnippet = new Chart(ctx_snippet,{
    type: 'pie',
    data: data_snippet,
    options: options_Snippet
  });
})
