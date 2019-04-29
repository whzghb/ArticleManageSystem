$(".detail").click(function () {
    var cur_url = window.location.href;
    var cur_id = $(this).attr("id_val");
    window.location.href = cur_url.split("?")[0] + "?id=" + cur_id;
});

$(".delete_obj").click(function () {
    var cur_url = window.location.href.split("?")[0];
    var cur_id = $(this).attr("id_val");
    $.ajax({
  			url: cur_url,
			type:'delete',
			headers: {"X-CSRFToken": $.cookie("csrftoken")},
			dataType:'json',
            data:{
                id: cur_id,
            },
			success:function(res){
				if(res.code=="200"){
			     	window.location.reload();
				}else{
					alert(res.msg);
				}
			},
			error : function(XMLHttpRequest, textStatus, errorThrown) {
				layer.alert('网络失败，请刷新页面后重试', {icon: 2});
			}
          })
});

