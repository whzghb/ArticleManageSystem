$(".login").click(function () {
   var name = $("#name").val();
   var password = $("#password").val();
   var url = "/user/login/"
   if (name == ""){
       alert("请输入用户名");
   }
   else if (password == ""){
       alert("请输入密码");
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
                },
                success: function (res) {
                    if (res.code == "200") {
                        window.location.href = "/";
                    } else {
                        $("#name").val(name);
				        $("#password").val(password);
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

$("#password").keydown(function () {
     var e = e || event,
	 keycode = e.which || e.keyCode;
	 if (keycode == 13){
	     var name = $("#name").val();
	     var password = $("#password").val();
         var url = "/user/login/"
         if (name == ""){
            alert("请输入用户名");
        }
        else if (password == ""){
            alert("请输入密码");
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
                 },
                 success: function (res) {
                     if (res.code == "200") {
                         window.location.href = "/";
                     } else {
                         $("#name").val(name);
				         $("#password").val(password);
                         alert(res.error);
                         // window.location.reload();
                     }
                 },
                 error: function (XMLHttpRequest, textStatus, errorThrown) {
                     alert("失败");
                 }
             })
         }
   }
});

