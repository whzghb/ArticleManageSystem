$(".detail").click(function () {
    var cur_url = window.location.href;
    var cur_id = $(this).attr("id_val");
    window.location.href = cur_url.split("?")[0] + "?id=" + cur_id;
});

$(".delete_obj").on("click", function () {
	var dele = confirm("确定删除吗");
	if(dele==true) {
        var cur_url = window.location.href.split("?")[0];
        var cur_id = $(this).attr("id_val");
        $.ajax({
            url: cur_url,
            type: 'delete',
            headers: {"X-CSRFToken": $.cookie("csrftoken")},
            dataType: 'json',
            data: {
                id: cur_id,
            },
            success: function (res) {
                if (res.code == "200") {
                    window.location.href = cur_url;
                } else {
                    alert(res.msg);
                }
            },
        })
    }
    $(this).unbind();
})

$(".submit_add").click(function () {
	var name = $(this).prev().val();
	if (name == ""){
			alert("不能为空");
		}
	else {
	var url = window.location.href;
	$.ajax({
				url: url,
				type:'post',
				headers: {"X-CSRFToken": $.cookie("csrftoken")},
				dataType:'json',
				data:{
					name: name,
				},
				success:function(res){
					if(res.code=="200"){
						window.location.reload();
					}else{
						alert(res.msg);
					}
				},
				error : function(XMLHttpRequest, textStatus, errorThrown) {
					alert("失败");
				}
			  })
	}
	$(this).unbind();
});

$(".logo").click(function () {
	window.location.href = "/";
});

$(".query").click(function () {
    var cur_url = window.location.href;
    var search = $(this).prev().val();
    window.location.href = cur_url.split("")[0] + "?page=1&search=" + search;
});

$("input[name='query']").keydown(function(e){
	 var e = e || event,
	 keycode = e.which || e.keyCode;
	 if (keycode==13) {
	  	$(".log_btn").trigger("click");
		var cur_url = window.location.href;
    	var search = $(this).val();
    	window.location.href = cur_url.split("?")[0] + "?page=1&search=" + search;
 	}
});

$("input[name='add']").keydown(function(){
	 var e = e || event,
	 keycode = e.which || e.keyCode;
	 if (keycode==13) {
	  	$(".log_btn").trigger("click");
		var name = $(this).val();
		if (name == ""){
			alert("不能为空");
		}
		else {
		var url = window.location.href;
		$.ajax({
					url: url,
					type:'post',
					headers: {"X-CSRFToken": $.cookie("csrftoken")},
					dataType:'json',
					data:{
						name: name,
					},
					success:function(res){
						if(res.code=="200"){
							window.location.reload();
						}else{
							alert(res.msg);
						}
					},
					error : function(XMLHttpRequest, textStatus, errorThrown) {
						alert("失败");
					}
				  })
 	}
	}
	$(this).unbind();
});


$(function () {
            var name = $.cookie("user_name");
            if (name == null){
                $('.user').html('<span><a href="/user/login/">登录</a></span>&nbsp;|&nbsp;<span><a href="/user/register/">注册</a></span>')
            }
            else {
            	if (name.indexOf("\\u")>0) {
                	var str = "";
                	var s = name.split('\\u');
                    for (var i = 0; i < s.length; i++) {
                        if (s[i].length > 4) {
                            str += String.fromCharCode(parseInt(s[i].slice(0, 4), 16)) + "\t";
                            str += s[i].slice(4, -1);
                        }
                        else {
                            str += String.fromCharCode(parseInt(s[i], 16)) + "\t";
                        }
                    }
                }
                else {
                    str = name.replace('"', '').replace('"', '');
                }
                $(".user").html('<span id="user">'+ str +'</span>&nbsp;|&nbsp;<span><a href="/user/logout/">注销</a></span>');
            }
        });
