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
                console.log("like increased");
            }
            else{
                likeCount--;
                $('#likeCount').html(likeCount);
                likeBtn.html('<i class="fa fa-heart-o" aria-hidden="true"style=color:#333333;"></i>');
                console.log("like decreased");

            }

        },
    });

});
