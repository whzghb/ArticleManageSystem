$(".register").click(function () {
   var name = $("#name").val();
   var password = $("#password").val();
   var re_password = $("#re_password").val();
   var url = "/user/register/"
   if (name == ""){
       alert("请输入用户名");
   }
   else if (password == ""){
       alert("请输入密码");
   }
   else if (re_password == ""){
       alert("请确认密码");
   }
   else if (password != re_password){
       alert("两次密码不一致");
   }
   else {
       $.ajax({
                url: url,
                type: "post",
                headers: {"X-CSRFToken": $.cookie("csrftoken")},
                dataType: 'json',
                data: {
                    name: name,
                    password: password,
                    re_password: re_password,
                },
                success: function (res) {
                    if (res.code == "200") {
                        alert("注册成功");
                        window.location.href = "/";
                    }
                    else {
                        $("#name").val(name);
				        $("#password").val(password);
				        $("#re_password").val(re_password);
                        alert(res.error);
                        // window.location.reload();
                    }
                },
                error: function (XMLHttpRequest, textStatus, errorThrown) {
                    alert("失败");
                }
            })
   }
});

$("#re_password").keydown(function () {
     var e = e || event,
	 keycode = e.which || e.keyCode;
	 if (keycode == 13){
	     var name = $("#name").val();
       var password = $("#password").val();
       var re_password = $("#re_password").val();
       var url = "/user/register/"
       if (name == ""){
           alert("请输入用户名");
       }
       else if (password == ""){
           alert("请输入密码");
       }
       else if (re_password == ""){
           alert("请确认密码");
       }
       else if (password != re_password){
           alert("两次密码不一致");
       }
       else {
           $.ajax({
               url: url,
               type: "post",
               headers: {"X-CSRFToken": $.cookie("csrftoken")},
               dataType: 'json',
               data: {
                   name: name,
                   password: password,
                   re_password: re_password,
               },
               success: function (res) {
                   if (res.code == "200") {
                       alert("注册成功");
                       window.location.href = "/";
                   } else {
                       $("#name").val(name);
				        $("#password").val(password);
				        $("#re_password").val(re_password);
                       alert(res.error);
                       // window.location.reload();
                   }
               },
               error: function (XMLHttpRequest, textStatus, errorThrown) {
                   alert("错误");
               }
           })
       }
   }
});