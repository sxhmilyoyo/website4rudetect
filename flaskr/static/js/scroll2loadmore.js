$(window).scroll(function() {
  console.log("1");
  console.log("1:"+$(window).scrollTop());
  console.log("2:"+$(document).height());
  console.log("3:"+$(window).height());
  console.log("3:" + $SCRIPT_ROOT + 'loadmore');
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
        for (var i = 0; i < pro.length; i++) {
          var dom =
            `
            <a class="list-link-item" data-toggle="collapse" data-target="#${pro[i][0]}" aria-expanded="false" aria-controls="${pro[i][0]}">
              <div class="media text-muted pt-3">
                <!-- <img data-src="holder.js/32x32?theme=thumb&bg=007bff&fg=007bff&size=1" alt="" class="mr-2 rounded"> -->
                <!-- <p class="d-inline-block text-truncate text-left media-body pb-3 mb-0 small lh-50 border-bottom border-gray" style="max-width: 1200px;"> -->
                <p class="text-truncate text-left media-body pb-3 mb-0 small lh-50 border-bottom border-gray">
                  <strong class="d-block text-gray-dark">@username</strong>
                  ${pro[i][1]}
                </p>
              </div>
            </a>
            <div id="${pro[i][0]}" class="collapse border-bottom border-gray bg-light" aria-labelledby="headingOne" data-parent="#accordion">
              <div class="wrapper text-right">
                <button class="opinion button button-3d button-circle mt-2 mb-3 mr-2" stance="FAVOR"><i class="fa fa-check"></i></button>
                <button class="opinion button button-3d button-circle mt-2 mb-3 mr-2" stance="AGAINST"><i class="fa fa-times"></i></button>
                <a href="https://twitter.com/anyuser/status/${pro[i][0]}" class="button button-3d button-circle mt-2 mb-3 mr-2"><i class="fa fa-info"></i></a>
              </div>
            </div>
            <script src="/static/js/addopinion.js?1532"></script>
            `;
          $("#listPro").append(dom);
        }
        for (var i = 0; i < con.length; i++) {
          var dom =
            `
            <a class="list-link-item" data-toggle="collapse" data-target="#${con[i][0]}" aria-expanded="false" aria-controls="${con[i][0]}">
              <div class="media text-muted pt-3">
                <!-- <img data-src="holder.js/32x32?theme=thumb&bg=007bff&fg=007bff&size=1" alt="" class="mr-2 rounded"> -->
                <!-- <p class="d-inline-block text-truncate text-left media-body pb-3 mb-0 small lh-50 border-bottom border-gray" style="max-width: 1200px;"> -->
                <p class="text-truncate text-left media-body pb-3 mb-0 small lh-50 border-bottom border-gray">
                  <strong class="d-block text-gray-dark">@username</strong>
                  ${con[i][1]}
                </p>
              </div>
            </a>
            <div id="${con[i][0]}" class="collapse border-bottom border-gray bg-light" aria-labelledby="headingOne" data-parent="#accordion">
              <div class="wrapper text-right">
                <button class="opinion button button-3d button-circle mt-2 mb-3 mr-2" stance="FAVOR"><i class="fa fa-check"></i></button>
                <button class="opinion button button-3d button-circle mt-2 mb-3 mr-2" stance="AGAINST"><i class="fa fa-times"></i></button>
                <a href="https://twitter.com/anyuser/status/${con[i][0]}" class="button button-3d button-circle mt-2 mb-3 mr-2"><i class="fa fa-info"></i></a>
              </div>
            </div>
            <script src="/static/js/addopinion.js?1532"></script>
            `;
          $("#listCon").append(dom);
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
//               <a class="list-link-item" href="https://twitter.com/anyuser/status/${pro[i][0]}">
//                 <div class="media text-muted pt-3">
//                   <img data-src="holder.js/32x32?theme=thumb&bg=007bff&fg=007bff&size=1" alt="" class="mr-2 rounded">
//                   <p class="media-body pb-3 mb-0 small lh-125 border-bottom border-gray">
//                     <strong class="d-block text-gray-dark">@username</strong>
//                       ${pro[i][2]}
//                   </p>
//                 </div>
//               </a>
//               `;
//           // var dom = '<a class="list-link-item" href="https://twitter.com/anyuser/status/"><div class="media text-muted pt-3"><img data-src="holder.min.js/32x32?theme=thumb&bg=007bff&fg=007bff&size=1" alt="" class="mr-2 rounded"><p class="media-body pb-3 mb-0 small lh-125 border-bottom border-gray"><strong class="d-block text-gray-dark">@username</strong>' + pro[i][2] + '</p></div></a>'
//           $("#listPro").append(dom);
//         }
//         for (var i = 0; i < con.length; i++) {
//           var dom = `
//               <a class="list-link-item" href="https://twitter.com/anyuser/status/${con[i][0]}">
//                 <div class="media text-muted pt-3">
//                   <img data-src="holder.js/32x32?theme=thumb&bg=007bff&fg=007bff&size=1" alt="" class="mr-2 rounded">
//                   <p class="media-body pb-3 mb-0 small lh-125 border-bottom border-gray">
//                     <strong class="d-block text-gray-dark">@username</strong>
//                       ${con[i][2]}
//                   </p>
//                 </div>
//               </a>
//               `;
//           // var dom = '<a class="list-link-item" href="https://twitter.com/anyuser/status/"><div class="media text-muted pt-3"><img data-src="holder.min.js/32x32?theme=thumb&bg=007bff&fg=007bff&size=1" alt="" class="mr-2 rounded"><p class="media-body pb-3 mb-0 small lh-125 border-bottom border-gray"><strong class="d-block text-gray-dark">@username</strong>' + pro[i][2] + '</p></div></a>'
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
