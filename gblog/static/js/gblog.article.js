// Get cookie _xsrf
function getCookie(name) {
    var r = document.cookie.match("\\b" + name + "=([^;]*)\\b");
    return r ? r[1] : undefined;
}

var reply_id = "";
var _xsrf = getCookie("_xsrf");
var email_reg = /^\w+((-\w+)|(\.\w+))*\@[A-Za-z0-9]+((\.|-)[A-Za-z0-9]+)*\.[A-Za-z]+$/;
var url_reg=/^((http|https|ftp):\/\/)?(\w(\:\w)?@)?([0-9a-z_-]+\.)*?([a-z0-9-]+\.[a-z]{2,6}(\.[a-z]{2})?(\:[0-9]{2,6})?)((\/[^?#<>\/\\*":]*)+(\?[^#]*)?(#.*)?)?$/i;

// Delete comment
function delete_comment(comment_id, entry_id) {
  if(confirm("Are you sure to DELETE it?")){
    obj=$.ajax({url:"/comment", data:{'_xsrf':_xsrf, 'id':comment_id, 'entry_id':entry_id}, dateType: "text", type: "DELETE", 
        success: function() {
            $( "#comments-"+comment_id ).slideUp(300);
            cnt= parseInt( $( "#comments-cnt").text() ); 
            $( "#comments-cnt" ).text(cnt>0?cnt-1:cnt);

        }});
  }
}
// Reply comment
function reply_comment(comment_id) {
    reply_id = comment_id;
    $("#comments-post").insertAfter( "#comments-"+comment_id );
    $("#comments-post-info").html('<a href="javascript:void(0)" onclick="cancel_reply()">cancel reply</a>');
}

// Cancel Reply comment
function cancel_reply(callback) {
    reply_id = "";
    $("#comments-post").insertAfter( "#comments-list" );
    $("#comments-post-info").html('<h3>Add a new comment:</h3>');
    callback();
}

// Delete article
function delete_article(entry_id) {
  if(confirm("Are you sure to DELETE it?")){
    obj=$.ajax({url:"/compose", data:{'_xsrf':_xsrf, 'entry_id':entry_id}, dateType: "text", type: "DELETE", 
        success: function() {
          location.href = "/";
        }});
  }
}

$(document).ready(function() {
  //load comments
  entry_id = $( "#entry_id" ).val();
  $( "#comments" ).load("/comment?id="+entry_id, function() {
  // Email validation
    $( "#email" ).blur(function( ) {
      if( $("#email").val()!==""){
        if(!email_reg.test($("#email").val())){
            $("#isemail").html('<p class="warnning">invalid email</p>')
                return false;
        }
        $("#isemail").html('<p class="pass">OK</p>');
      } else {
        $("#isemail").html('*');
      }
    });
    // URL validation
    $( "#url" ).blur(function( ) {
      if( $("#url").val()!==""){
        if(!url_reg.test($("#url").val())){
          $("#isurl").html('<p class="warnning">invalid URL</p>')
              return false;
        }
        $("#isurl").html('<p class="pass">OK</p>');
      }else{
        $("#isurl").html('');
      }

    });
    // // Add a comment 
    // Attach a submit handler to the form
    $("form#addreply").submit(function( event ) {
      var required = ["author", "email", "content"];
      var form = $(this).get(0);
      for (var i = 0; i < required.length; i++) {
          if (!form[required[i]].value) {
              $(form[required[i]]).select();
              return false;
          }
      }
      // Stop form from submitting normally
      event.preventDefault();
      // Get some values from elements on the page:
      var $form = $( this ),
      //_xsrf = $form.find( "input[name='_xsrf']" ).val(),
      author = $form.find( "input[name='author']" ).val(),
      email = $form.find( "input[name='email']" ).val(),
      website = $form.find( "input[name='url']" ).val(),
      content = $form.find( "textarea[name='content']" ).val(),
      url = $form.attr( "action" );
      // test email  
      if(!email_reg.test(email)){
          $(form["email"]).select();
          return false;
      }
      // test url if existed
      if( $("#url").val()!==""){
        if(!url_reg.test($("#url").val())){
          $(form["url"]).select();
          return false;
        }
      }
      // Send the data using post
      var posting = $.post( url, { 'id':entry_id, 'author':author, 'email':email, 'url':website, 'content':content, '_xsrf':_xsrf, 'reply_id':reply_id } );
      posting.done(function( data ) {
        $( "#comments-list" ).append(data);
        document.getElementById('content').value="";
        cnt=$( "#comments-cnt").text();
        $( "#comments-cnt" ).text(parseInt(cnt)+1);
        if( parseInt(cnt) == 0) {
            $("#no-comments").remove();
        }
        if( reply_id ) {
          cancel_reply(function () {
          $("html,body").animate({scrollTop: $("#comments-post").offset().top-400}, 200);
          });
        }
      });
    });
  });
});
