
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
    var commentcount=event.querySelector('.commentcount2').value;
    commentcount=Number(commentcount)+1;
    console.log(commentcount);

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
            console.log(result);
            console.log(result.text);
            var final_comment=result.text;
            console.log(updatedlength);
            if(final_comment.length>0){
                event.querySelector('.commentcount').innerHTML=commentcount;
               if(updatedlength==0){
                   var cc= '<span class="updated2"><span><strong class="cmntuser">'+user+'</strong><span class="cmnttext">'+" "+final_comment+'</span></span></span>';
                   event.querySelector('.updated1').innerHTML=cc;
                   event.querySelector('.comment_box').value='';
                   console.log("comment Successful 1");
               }
               else if(updatedlength==1) {
                   event.querySelector('.updated2').insertAdjacentHTML('beforeend'," <br/><span><strong>" + user + "</strong><span>" + " "+final_comment + "</span></span>");
                   event.querySelector('.comment_box').value='';
                   console.log("comment Successful 2");
               }
               else if(updatedlength>1) {
                   event.querySelector('.updated1').insertAdjacentHTML('beforeend'," <span><span><strong>" + user + "</strong><span>" + " "+final_comment + "</span></span></span><br/>");
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

$('.searchbar').on('click',function(){
   $('.searchbar').css('padding-left','28px').css('background-color','white');
   $('.searchIcon').css('padding-left','8px');
});



function searchUser(event) {
    var userName= $('.searchbar').val();
    console.log(userName);
    if(userName.length>0 && event.keyCode!=8){
        $.ajax({
       method:'POST',
       url:'/search_user/',
       dataType:'json',
       beforeSend: function () {
          $('#loader').removeClass('hidden');
          if($('.errormessage').hasClass('hidden')==false){
              $('.errormessage').toggleClass('hidden');
          }
       },
       data:{
           'userName':userName,
           'csrfmiddlewaretoken':event.querySelector('input[name=csrfmiddlewaretoken]').value
       },
        success:function (response) {
           if(response.searchresult){
               var obj=JSON.parse(response.searchresult);
               console.log(obj);
               $('#searchResults').show();

               var names=[];
               var usernames=[];
               for(i=0;i<obj.length;i++){
                names.push(obj[i].fields["name"]);
                usernames.push(obj[i].fields["username"]);
               }
               console.log(names+usernames);
               var existingnames=[];
               var existingusernames=[];
               for(i=0;i<$('.searchedname').length;i++){
                   var searchednames=$('.searchedname').eq( i ).html();;
                   var searchedusernames=$('.searchedUsername').eq( i ).html();;
                   existingnames.push(searchednames);
                   existingusernames.push(searchedusernames);
               }
               console.log(existingnames+existingusernames);
                /*var input = document.createElement('input');
                input.type = 'hidden';
                input.name = 'csrfmiddlewaretoken';
                input.value = '{% csrf_token %}';*/
               for(i=0;i<names.length;i++){
                   console.log(names[i]+usernames[i]);
                    if(existingnames.indexOf(names[i].toUpperCase())==-1 && existingusernames.indexOf(usernames[i]==-1)){

                       for(i=0;i<obj.length;i++){
                         console.log(obj[i].fields['username']);
                         var html='<div class="container-fluid searchedUserContainer"> <div class="row"> <div class="col-md-3"> <img src="https://i.imgur.com/vMfyeUG.jpg" class="searchedDisplayPic"> </div><div class="col-md-9"style="padding-left: 0px;"> <form class="viewprofile"action="/profile_by_search/"method="post"onclick="submitform(this);"><p class="searchedUsername"" >'+usernames[i]+'</p><input type="hidden"name="username"value='+usernames[i]+'></form><p class="searchedname">'+names[i].toUpperCase()+'</p></div></div></div>';
                            $('#searchResults').append(html);

                    }
               }


               }
               $('#loader').addClass('hidden');
                $('#cross').removeClass('hidden');
           }
           else if(response.message){
               console.log(response.message);
               $('.errormessage').html(response.message).toggleClass('hidden');
               $('#searchResults').show();
               $('.searchedUserContainer').remove();
               $('#loader').addClass('hidden');

           }

        },
    });
    }
    else{
        $('#searchResults').hide();
    }
}

$('.fa-close').on('click',function(){
   $('#cross').addClass('hidden');
   $('.searchbar').blur().css('padding-left','75px');
   $('.searchbar').val("");
   $('.searchIcon').css('padding-left','56px');
   $('#searchResults').hide();
   $('.searchedUserContainer').remove();
});

function profile_by_search(event) {
    var username=event.querySelector('.searchedUsername').innerHTML;
    console.log(username);
    $.ajaxSetup({
        headers: { "X-CSRFToken": getCookie("csrftoken") }
    });
    $.ajax({
        method:'POST',
        url: '/profile_by_search/',
        data: {
            'username':username,
    },

    });

}

function getCookie(c_name)
{
    if (document.cookie.length > 0)
    {
        c_start = document.cookie.indexOf(c_name + "=");
        if (c_start != -1)
        {
            c_start = c_start + c_name.length + 1;
            c_end = document.cookie.indexOf(";", c_start);
            if (c_end == -1) c_end = document.cookie.length;
            return unescape(document.cookie.substring(c_start,c_end));
        }
    }
    return "";
 }


 function submitform(event) {
     event.submit();
 }