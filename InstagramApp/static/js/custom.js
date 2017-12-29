$('#likeForm').on('click',function(){
    var postId=$("#postId").val();
    var likeCount=$('#likeCount').html();
    var likeBtn=$('.like');
    $.ajax({
        method:'POST',
        url:'/like/',
        dataType:'json',
        data:{
            'postId':postId,
            'csrfmiddlewaretoken':$('input[name=csrfmiddlewaretoken]').val()
        },
        success:function(result){
            console.log(result.flag);
            if(result.flag==true){
                likeCount++;
                $('#likeCount').html(likeCount);
                likeBtn.html('<i class="fa fa-heart" aria-hidden="true"style=color:#ed4956;"></i>');
                $('#bigLike').removeClass('hidden');
                setTimeout(function(){ $('#bigLike').addClass('hidden'); }, 1300);
                console.log("like increased");
            }
            else{
                likeCount--;
                $('#likeCount').html(likeCount);
                likeBtn.html('<i class="fa fa-heart-o" aria-hidden="true"style=color:#333333;"></i>');
                $('#bigUnlike').removeClass('hidden');
                setTimeout(function(){ $('#bigUnlike').addClass('hidden'); }, 1300);
                console.log("like decreased");

            }

        },
    });

});



$('#commentBtn').on('click',function(){
    var cmntPostId=$('#cmntPostId').val();
    var commentText=$('.comment_box').val();
    var user=$('.hiddenUser').text();
    var updatedlength=$('.updated2').length;

    console.log(commentText);
    $.ajax({
        method:'POST',
        url:'/comment/',
        dataType:'json',
        data:{
            'cmntPostId':cmntPostId,
            'commentText':commentText,
            'csrfmiddlewaretoken':$('input[name=csrfmiddlewaretoken]').val()
        },
        success:function(result){
            console.log(result.text);
            var final_comment=result.text;
            console.log(updatedlength);
            if(final_comment.length>0){
               if(updatedlength==0){
                   var cc= '<span class="updated2"><span><strong class="cmntuser">'+user+'</strong><span class="cmnttext">'+final_comment+'</span></span></span>';
                   $('.updated1').html(cc);
                   $('.comment_box').val('');
                   console.log("comment Successful 1");
               }
               else if(updatedlength==1) {
                   $('.updated2').append(" <br/><span><strong>" + user + "</strong><span>" + final_comment + "</span></span>");
                   $('.comment_box').val('');
                   console.log("comment Successful 2");
               }
               else if(updatedlength>1) {
                   $('.updated1').append(" <span><span><strong>" + user + "</strong><span>" + final_comment + "</span></span></span><br/>");
                   $('.comment_box').val('');
                   console.log("comment Successful 3");
               }
            }
            else{
                console.log("comment unsuccessful");

            }
        },
    });
});

$(document).ready(function(){
    $('[data-toggle="tooltip"]').tooltip();
});

$('#commentIcon').on('click',function () {
   $('.comment_box').focus();
});