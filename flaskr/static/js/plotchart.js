$('#nav-tab #nav-chart-tab').on('shown.bs.tab', function (e) {
// $('a[data-toggle="tab"]').on('show.bs.tab', function (e) {
  console.log("test");
  var ctx = $("#myChart");
  var data = {
    datasets: [{
        label: "Percentage of Stance",
        data: [10, 20],
        backgroundColor: [
                'rgb(255, 99, 132)',
                'rgb(255, 205, 86)'
            ],
        borderWidth: 3
    }],
    // These labels appear in the legend and in the tooltips when hovering different arcs
    labels: [
        'FAVOR',
        'AGAINST'
    ]
  };
  var options = {
    responsive: true,
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
            text: 'Percentage of Stance',
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
  var myPieChart = new Chart(ctx,{
    type: 'pie',
    data: data,
    options: options
  });

})
