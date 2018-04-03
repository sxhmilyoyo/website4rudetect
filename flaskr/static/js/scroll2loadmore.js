$(window).scroll(function() {
  // console.log("1");
  // console.log("1:"+$(window).scrollTop());
  // console.log("2:"+$(document).height());
  // console.log("3:"+$(window).height());
  // console.log("3:" + $SCRIPT_ROOT + 'loadmore');
  if ($(window).scrollTop()>0 && $(window).scrollTop() == $(document).height() - $(window).height()) {
    $.getJSON($SCRIPT_ROOT + '/loadmore',
      function(data) {
        // if (e.data.flag == 'pro') {
        //   var tweets = data.pro;
        //   var tag = '#listPro';
        // } else if (e.data.flag == 'con') {
        //   var tweets = data.con;
        //   var tag = '#listCon
        // }
        // console.log(e.data.flag);
        var pro = data.pro;
        var con = data.con;
        var idx = data.idx;
        for (var i = 0; i < pro.length; i++) {
          var dom =
            `
            <a class="list-link-item" style="display: none;" data-toggle="collapse" data-target="#${pro[i][1]}" aria-expanded="false" aria-controls="${pro[i][1]}">
              <div class="media text-muted pt-3">
                <!-- <img data-src="der.js/32x32?theme=thumb&bg=007bff&fg=007bff&size=1" alt="" class="mr-2 rounded"> -->
                <!-- <p class="d-inline-block text-truncate text-left media-body pb-3 mb-0 small lh-50 border-bottom border-gray" style="max-width: 1200px;"> -->
                <div class="color-box my-1 mr-2 rounded text-white text-center" style="background-color: #ee4d4d;">${i+idx+1}</div>
                <p class="text-truncate text-left media-body pb-3 mb-0 small lh-50 border-bottom border-gray">
                  <strong class="d-block text-gray-dark">${pro[i][0]}</strong>
                  ${pro[i][2]}
                </p>
              </div>
            </a>
            <div id="${pro[i][1]}" class="collapse border-bottom border-gray bg-light" aria-labelledby="headingOne" data-parent="#accordion">
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
                    <a href="https://twitter.com/anyuser/status/${pro[i][1]}" class="button button-3d button-circle mt-2 mb-3 mr-2"><i class="fa fa-info"></i></a>
                  </div>
                </div>
              </div>
            </div>

            `;
          $("#listPro").append(dom);
          $("#listPro > .list-link-item:hidden").each(function(i, obj) {
            console.log("pro", i);
            var row = $(this);
            setTimeout(function() {
              row.show(800);
            }, 200*i);
          });
          // $('.list-link-item').show(1000);
          // setTimeout(function() { $("#listPro").append(dom); }, 300);
        }
        for (var i = 0; i < con.length; i++) {
          var dom =
            `
            <a class="list-link-item" style="display: none;" data-toggle="collapse" data-target="#${con[i][1]}" aria-expanded="false" aria-controls="${con[i][1]}">
              <div class="media text-muted pt-3">
                <!-- <img data-src="der.js/32x32?theme=thumb&bg=007bff&fg=007bff&size=1" alt="" class="mr-2 rounded"> -->
                <!-- <p class="d-inline-block text-truncate text-left media-body pb-3 mb-0 small lh-50 border-bottom border-gray" style="max-width: 1200px;"> -->
                <div class="color-box my-1 mr-2 rounded text-white text-center" style="background-color: #2b2e48;">${i+idx+1}</div>
                <p class="text-truncate text-left media-body pb-3 mb-0 small lh-50 border-bottom border-gray">
                  <strong class="d-block text-gray-dark">${con[i][0]}</strong>
                  ${con[i][2]}
                </p>
              </div>
            </a>
            <div id="${con[i][1]}" class="collapse border-bottom border-gray bg-light" aria-labelledby="headingOne" data-parent="#accordion">
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
                    <a href="https://twitter.com/anyuser/status/${con[i][1]}" class="button button-3d button-circle mt-2 mb-3 mr-2"><i class="fa fa-info"></i></a>
                  </div>
                </div>
              </div>
            </div>

            `;
          $("#listCon").append(dom);
          $("#listCon > .list-link-item:hidden").each(function(i, obj) {
            console.log("con", i);
            var row = $(this);
            setTimeout(function() {
              row.show(800);
            }, 200*i);
          });
        }
      });
  }
});

// $(function() {
//   var submit_form = function(e) {
//     $.getJSON($SCRIPT_ROOT + '/loadmore',
//       function(data) {
//         // if (e.data.flag == 'pro') {
//         //   var tweets = data.pro;
//         //   var tag = '#listPro';
//         // } else if (e.data.flag == 'con') {
//         //   var tweets = data.con;
//         //   var tag = '#listCon';
//         // }
//         // console.log(e.data.flag);
//         var pro = data.pro;
//         var con = data.con;
//         for (var i = 0; i < pro.length; i++) {
//
//           var dom = `
//               <a class="list-link-item" href="https://twitter.com/anyuser/status/${pro[i][1]}">
//                 <div class="media text-muted pt-3">
//                   <img data-src="der.js/32x32?theme=thumb&bg=007bff&fg=007bff&size=1" alt="" class="mr-2 rounded">
//                   <p class="media-body pb-3 mb-0 small lh-125 border-bottom border-gray">
//                     <strong class="d-block text-gray-dark">@username</strong>
//                       ${pro[i][2]}
//                   </p>
//                 </div>
//               </a>
//               `;
//           // var dom = '<a class="list-link-item" href="https://twitter.com/anyuser/status/"><div class="media text-muted pt-3"><img data-src="der.min.js/32x32?theme=thumb&bg=007bff&fg=007bff&size=1" alt="" class="mr-2 rounded"><p class="media-body pb-3 mb-0 small lh-125 border-bottom border-gray"><strong class="d-block text-gray-dark">@username</strong>' + pro[i][2] + '</p></div></a>'
//           $("#listPro").append(dom);
//         }
//         for (var i = 0; i < con.length; i++) {
//           var dom = `
//               <a class="list-link-item" href="https://twitter.com/anyuser/status/${con[i][1]}">
//                 <div class="media text-muted pt-3">
//                   <img data-src="der.js/32x32?theme=thumb&bg=007bff&fg=007bff&size=1" alt="" class="mr-2 rounded">
//                   <p class="media-body pb-3 mb-0 small lh-125 border-bottom border-gray">
//                     <strong class="d-block text-gray-dark">@username</strong>
//                       ${con[i][2]}
//                   </p>
//                 </div>
//               </a>
//               `;
//           // var dom = '<a class="list-link-item" href="https://twitter.com/anyuser/status/"><div class="media text-muted pt-3"><img data-src="der.min.js/32x32?theme=thumb&bg=007bff&fg=007bff&size=1" alt="" class="mr-2 rounded"><p class="media-body pb-3 mb-0 small lh-125 border-bottom border-gray"><strong class="d-block text-gray-dark">@username</strong>' + pro[i][2] + '</p></div></a>'
//           $("#listCon").append(dom);
//         }
//         // $('#listPro').text(pro[i]);
//         // $('input[name=a]').focus().select();
//       });
//     return false;
//   };
//
//   $('button#loadmore').bind('click', submit_form);
//   // $('button#loadmore-pro').click({
//   //   flag: "pro"
//   // }, submit_form);
//   // $('button#loadmore-con').click({
//   //   flag: "con"
//   // }, submit_form);
//   // $('input[type=text]').bind('keydown', function(e) {
//   //   if (e.keyCode == 13) {
//   //     submit_form(e);
//   //   }
//   // });
//   // $('input[name=a]').focus();
// });
