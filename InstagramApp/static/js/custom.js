
$('.fa-comments-o ,.caption,.comment_box,.comments').click(false);

function likefunction(event){
    var postId=event.querySelector("#postId").value;
    var likeCount=event.querySelector("[name=likeCount]").innerHTML;
    var likeBtn=event.querySelector('.like');

    $.ajax({
        method:'POST',
        url:'/like/',
        dataType:'json',
        data:{
            'postId':postId,
            'csrfmiddlewaretoken':event.querySelector('input[name=csrfmiddlewaretoken]').value
        },
        success:function(result){
            console.log(result.flag);
            if(result.flag==true){
                likeCount++;
                event.querySelector("[name=likeCount]").innerHTML=likeCount;
                likeBtn.innerHTML='<i class="fa fa-heart" aria-hidden="true"style=color:#ed4956;"></i>';
                /*this code is long
                event.querySelector('[name=caption').insertAdjacentHTML('beforebegin','<i class="fa fa-heart bigHeart1 animated pulse"name="bigLike"id="bigLike" aria-hidden="true"style=""></i>');
                var red='<i class="fa fa-heart bigHeart1 animated pulse"name="bigLike"id="bigLike" aria-hidden="true"style=" "></i>';
                setTimeout(function(red){ event.querySelector('[name=bigLike]').remove(red); }, 1300);
                */
                event.querySelector('[name=bigLike]').style.display='block';
                setTimeout(function(){ event.querySelector('[name=bigLike]').style.display='none';}, 1300);
                console.log("like increased");
            }
            else{
                likeCount--;
                event.querySelector("[name=likeCount]").innerHTML=likeCount;
                likeBtn.innerHTML='<i class="fa fa-heart-o" aria-hidden="true"style=color:#333333;"></i>';
               /* event.querySelector('[name=caption').insertAdjacentHTML('beforebegin','<i class="fa fa-heart bigHeart2 animated pulse"name="bigUnlike"id="bigUnlike" aria-hidden="true"style=""></i>');
                var white='<i class="fa fa-heart bigHeart2 animated pulse"name="bigUnlike"id="bigUnlike" aria-hidden="true"style=""></i>';
                setTimeout(function(white){ event.querySelector('[name=bigUnlike]').remove(white); }, 1300);
                */
                event.querySelector('[name=bigUnlike]').style.display='block';
                setTimeout(function(){ event.querySelector('[name=bigUnlike]').style.display='none';}, 1300);
                console.log("like decreased");

            }

        },
    });

};


function commentFunction(event){
    var cmntPostId=event.querySelector('#cmntPostId').value;
    var commentText=event.querySelector('.comment_box').value;
    var user=event.querySelector('.hiddenUser').innerHTML;
    var updatedlength=event.getElementsByClassName('updated2').length;

    console.log(commentText);
    $.ajax({
        method:'POST',
        url:'/comment/',
        dataType:'json',
        data:{
            'cmntPostId':cmntPostId,
            'commentText':commentText,
            'csrfmiddlewaretoken':event.querySelector('input[name=csrfmiddlewaretoken]').value
        },
        success:function(result){
            console.log(result.text);
            var final_comment=result.text;
            console.log(updatedlength);
            if(final_comment.length>0){
               if(updatedlength==0){
                   var cc= '<span class="updated2"><span><strong class="cmntuser">'+user+'</strong><span class="cmnttext">'+final_comment+'</span></span></span>';
                   event.querySelector('.updated1').innerHTML=cc;
                   event.querySelector('.comment_box').value='';
                   console.log("comment Successful 1");
               }
               else if(updatedlength==1) {
                   event.querySelector('.updated2').insertAdjacentHTML('beforeend'," <br/><span><strong>" + user + "</strong><span>" + final_comment + "</span></span>");
                   event.querySelector('.comment_box').value='';
                   console.log("comment Successful 2");
               }
               else if(updatedlength>1) {
                   event.querySelector('.updated1').insertAdjacentHTML('beforeend'," <span><span><strong>" + user + "</strong><span>" + final_comment + "</span></span></span><br/>");
                    event.querySelector('.comment_box').value='';
                   console.log("comment Successful 3");
               }
            }
            else{
                console.log("comment unsuccessful");

            }
        },
    });
};

$(document).ready(function(){
    $('[data-toggle="tooltip"]').tooltip();
});


function focusFunction(e) {
   var f=e.querySelector('.comment_box')
       f.focus();
};