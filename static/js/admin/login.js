$('#login').click(function () {
    var name = $('#name').val();
    var password = $('#password').val();
    if(name == ""){
        alert("请输入用户名");
    }
    else if(password == "") {
        alert("请输入密码");
    }
    else{
          $.ajax({
  			url:'/admin/login/',
			type:'post',
            headers: {"X-CSRFToken": $.cookie("csrftoken")},
			dataType:'json',
            data:{
                email: name,
                password: password,
            },
			success:function(res){
				if(res.code==200){
			     	location.href = '/admin/main/';
				}else{
				    $("#name").val(name);
				    $("#password").val(password);
					alert(res.msg);
				}
			},
			error : function(XMLHttpRequest, textStatus, errorThrown) {
				alert("网络错误");
			}
          })
      }
})

$("#password").keydown(function () {
     var e = e || event,
	 keycode = e.which || e.keyCode;
	 if (keycode == 13){
	     var name = $('#name').val();
         var password = $('#password').val();
         if(name == ""){
            alert("请输入用户名");
         }
        else if(password == "") {
            alert("请输入密码");
        }
        else{
          $.ajax({
  			url:'/admin/login/',
			type:'post',
            headers: {"X-CSRFToken": $.cookie("csrftoken")},
			dataType:'json',
            data:{
                email: name,
                password: password,
            },
			success:function(res){
				if(res.code==200){
			     	location.href = '/admin/main/';
				}else{
				    $("#name").val(name);
				    $("#password").val(password);
					alert(res.msg);
				}
			},
			error : function(XMLHttpRequest, textStatus, errorThrown) {
				alert("网络错误");
			}
          })
      }
	 }
});

