$("#loadmore").on('click', function (e) {
 
  $.getJSON('/loadmore',
    function (data) {
      // if (e.data.flag == 'pro') {
      //   var tweets = data.pro;
      //   var tag = '#listPro';
      // } else if (e.data.flag == 'con') {
      //   var tweets = data.con;
      //   var tag = '#listCon
      // }
      console.log(data);
      console.log("data");
      var support = data.support;
      var oppose = data.oppose;
      var idx = data.idx;
      for (var i = 0; i < support.length; i++) {
        var dom =
          `
          <a class="list-link-item border-bottom border-gray" style="display: none;" data-toggle="collapse" href="#${support[i][1]}" aria-expanded="false">
            <div class="media text-muted pt-3">
              <!-- <img data-src="der.js/32x32?theme=thumb&bg=007bff&fg=007bff&size=1" alt="" class="mr-2 rounded"> -->
              <!-- <p class="d-inline-block text-truncate text-left media-body pb-3 mb-0 small lh-50 border-bottom border-gray" style="max-width: 1200px;"> -->
              <div class="color-box my-1 mr-2 rounded text-white text-center" style="background-color: #ee4d4d;">
                <p class="mt-1">
                  ${i + idx + 1}
                </p>
              </div>
              <p class="tsp text-left media-body pb-3 mb-0 small lh-50">
                <strong class="d-block text-gray-dark">
                  <font size="3">
                  ${support[i][0]}
                  </font>
                </strong>
                <font size="4">
                ${support[i][2]}
                </font>
              </p>
            </div>
          </a>
          <div id="${support[i][1]}" class="collapse border-bottom border-gray bg-light">
            <div class="row">
              <div class="col-7 alert_add">
                <div class="inserted alert-inline alert-success" role="alert" style="display: none">
                  submitted successfully!
                </div>
                <div class="updated alert-inline alert-warning" role="alert" style="display: none">
                  updated successfully!
                </div>
                <div class="existed alert-inline alert-danger" role="alert" style="display: none">
                  duplicate action!
                </div>
              </div>
              <div class="col-5">
                <div class="wrapper float-right">
                  <button class="opinion button button-3d button-circle mt-2 mb-3 mr-2" stance="FAVOR"><i class="fa fa-check"></i></button>
                  <button class="opinion button button-3d button-circle mt-2 mb-3 mr-2" stance="AGAINST"><i class="fa fa-times"></i></button>
                  <a href="https://twitter.com/anyuser/status/${support[i][1]}" class="button button-3d button-circle mt-2 mb-3 mr-2"><i class="fa fa-info"></i></a>
                </div>
              </div>
            </div>
          </div>

          `;
        $("#listSupportTweets").append(dom);
        $("#listSupportTweets > .list-link-item:hidden").each(function (i, obj) {
          console.log("pro", i);
          var row = $(this);
          setTimeout(function () {
            row.show(800);
          }, 200 * i);
        });
        // $('.list-link-item').show(1000);
        // setTimeout(function() { $("#listPro").append(dom); }, 300);
      }
      for (var i = 0; i < oppose.length; i++) {
        var dom =
          `
          <a class="list-link-item border-bottom border-gray" style="display: none;" data-toggle="collapse" data-target="#${oppose[i][1]}" aria-expanded="false" aria-opposetrols="${oppose[i][1]}">
            <div class="media text-muted pt-3">
              <!-- <img data-src="der.js/32x32?theme=thumb&bg=007bff&fg=007bff&size=1" alt="" class="mr-2 rounded"> -->
              <!-- <p class="d-inline-block text-truncate text-left media-body pb-3 mb-0 small lh-50 border-bottom border-gray" style="max-width: 1200px;"> -->
              <div class="color-box my-1 mr-2 rounded text-white text-center" style="background-color: #2b2e48;">
                <p class="mt-1">
                  ${i + idx + 1}
                </p>
              </div>
              <p class="tsp text-left media-body pb-3 mb-0 small lh-50">
                <strong class="d-block text-gray-dark">
                  <font size="3">
                  ${oppose[i][0]}
                  </font>
                </strong>
                <font size="4">
                ${oppose[i][2]}
                </font>
              </p>
            </div>
          </a>
          <div id="${oppose[i][1]}" class="collapse border-bottom border-gray bg-light" aria-labelledby="headingOne" data-parent="#accordion">
            <div class="row">
              <div class="col-7 alert_add">
                <div class="inserted alert-inline alert-success" role="alert" style="display: none">
                  submitted successfully!
                </div>
                <div class="updated alert-inline alert-warning" role="alert" style="display: none">
                  updated successfully!
                </div>
                <div class="existed alert-inline alert-danger" role="alert" style="display: none">
                  duplicate action!
                </div>
              </div>
              <div class="col-5">
                <div class="wrapper float-right">
                  <button class="opinion button button-3d button-circle mt-2 mb-3 mr-2" stance="FAVOR"><i class="fa fa-check"></i></button>
                  <button class="opinion button button-3d button-circle mt-2 mb-3 mr-2" stance="AGAINST"><i class="fa fa-times"></i></button>
                  <a href="https://twitter.com/anyuser/status/${oppose[i][1]}" class="button button-3d button-circle mt-2 mb-3 mr-2"><i class="fa fa-info"></i></a>
                </div>
              </div>
            </div>
          </div>

          `;
        $("#listOpposeTweets").append(dom);
        $("#listOpposeTweets > .list-link-item:hidden").each(function (i, obj) {
          console.log("con", i);
          var row = $(this);
          setTimeout(function () {
            row.show(800);
          }, 200 * i);
        });
      }
    });
  
});