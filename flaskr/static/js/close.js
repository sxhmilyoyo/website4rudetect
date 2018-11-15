$('#close-chart').on('click', function (e) {
    // $('a[data-toggle="tab"]').on('show.bs.tab', function (e) {
    console.log("close");
    $("#myChartTweet").remove();
    $("#tweet-canvass").append('<canvas id="myChartTweet" width="450px" height="450px"></canvas>');

    $("#myChartSnippet").remove();
    $("#snippet-canvass").append('<canvas id="myChartSnippet" width="450px" height="450px"></canvas>');
    })
    