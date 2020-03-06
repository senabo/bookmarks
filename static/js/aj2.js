 var csrftoken = Cookies.get('csrftoken');
    function csrfSafeMethod(method) {

      // these HTTP methods do not require CSRF protection
      return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }
    $.ajaxSetup({
      beforeSend: function(xhr, settings) {
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
          xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
      }
    });
    $(document).ready(function(){
        $('a.like').click(function(e){

    e.preventDefault();
    var url = $('#Url').attr('data-url');
    // var url = "http://127.0.0.1:8000/images/like/";
    $.post(url,
      {
        id: $(this).data('id'),
        action: $(this).data('action')
      },
      function(data){
        if (data['status'] == 'ok')
        {console.log('tess');
          var previous_action = $('a.like').data('action');

          // toggle data-action
          $('a.like').data('action', previous_action == 'like' ? 'unlike' : 'like');
          // toggle link text
          $('a.like').text(previous_action == 'like' ? 'Unlike' : 'Like');

          // update total likes
          var previous_likes = parseInt($('span.count .total').text());
          $('span.count .total').text(previous_action == 'like' ? previous_likes + 1 : previous_likes - 1);
        }
      }
    );
  });
       });