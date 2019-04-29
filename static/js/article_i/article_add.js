//详情页保存至待审核
$(".detail_audit").click(function () {
    var  cur_id = $(this).attr("id_val");
    var jump_url = "/admin/article_i/draft/";
    var cur_url = "/admin/article_i/s_c/to_audit/";
    status_change(2, cur_url=cur_url, cur_id=cur_id, jump_url, reject_reason="")
});

function removeWordXml(text){
  var html = text;
  html = html.replace(/<\/?SPANYES[^>]*>/gi, "");//  Remove  all  SPAN  tags
  html = html.replace(/<(\w[^>]*)  lang=([^|>]*)([^>]*)/gi, "<$1$3");//  Remove  Lang  attributes
  html = html.replace(/<\\?\?xml[^>]*>/gi, "");//  Remove  XML  elements  and  declarations
  html = html.replace(/<\/?\w+:[^>]*>/gi, "");//  Remove  Tags  with  XML  namespace  declarations:  <o:p></o:p>
  html = html.replace(/\n(\n)*( )*(\n)*\n/gi, '\n');
  html = html.replace(/&lt;/g, "<").replace(/&gt;/g, ">")
      .replace(/&amp;/g, "&");
  html = html.replace(/<br>/gi, "/r/n");
  html = html.replace(/&nbsp;/gi, " ");
  html = html.replace(/\ +/gi,"");
  return html;
}


function draft_or_audit(status, cur_url, cur_id="") {
    var author = $("#author").val();
    var title = $("#title").val();
    var content = editor.txt.html();
    // var content = removeWordXml(all_content);
    var category = $("input[name='category']:checked").val();
    var feng_mian = $("#img").attr("src");
    var tags = [];
    $("input[name='tag']:checked").each(function () {
        tags.push($(this).val());
    });
    if (author == ""){
        alert("请输入作者");
    }
    else if (title == ""){
        alert("请输入标题");
    }
    else if (content == ""){
        alert("请输入内容");
    }
    else if (category == ""){
        alert("请选择分类");
    }
    else if (tags == []) {
        alert("请选择标签");
    }
    else if (feng_mian == "") {
        alert("请选择封面");
    }
    else {
        if (cur_id != "") {
            $.ajax({
                url: cur_url,
                type: "put",
                headers: {"X-CSRFToken": $.cookie("csrftoken")},
                dataType: 'json',
                data: {
                    id: cur_id,
                    author: author,
                    title: title,
                    content: content,
                    img: feng_mian,
                    category_id: category,
                    tags: tags.toString(),
                    status: status,
                },
                success: function (res) {
                    if (res.code == "200") {
                        alert("操作成功");
                        window.location.href = "/admin/article_i/draft/";
                    } else {
                        alert(res.msg);
                        $("#content", parent.document.body).attr("src", cur_url);
                    }
                },
                error: function (XMLHttpRequest, textStatus, errorThrown) {
                    layer.alert('网络失败，请刷新页面后重试', {icon: 2});
                }
            })
        }
        else {
            $.ajax({
                url: cur_url,
                type: "POST",
                headers: {"X-CSRFToken": $.cookie("csrftoken")},
                dataType: 'json',
                data: {
                    author: author,
                    title: title,
                    content: content,
                    img: feng_mian,
                    category_id: category,
                    tags: tags.toString(),
                    status: status,
                },
                success: function (res) {
                    if (res.code == "200") {
                        alert("操作成功");
                        window.location.href = "/admin/article_i/draft/";
                    } else {
                        alert(res.msg);
                        // $("#content", parent.document.body).attr("src", cur_url);
                    }
                },
                error: function (XMLHttpRequest, textStatus, errorThrown) {
                    alert("权限不足");
                }
            })
        }
    }
}

function status_change(status, cur_url, cur_id, jump_url, reject_reason) {
    $.ajax({
  			url: cur_url,
			type:'put',
            headers: {"X-CSRFToken": $.cookie("csrftoken")},
			dataType:'json',
            data:{
  			    id: cur_id,
                status: status,
                reject_reason: reject_reason,
            },
			success:function(res){
				if(res.code=="200"){
				    alert("操作成功");
				    window.location.href = jump_url;
				}else{
					alert(res.msg);
				}
			},
			error : function(XMLHttpRequest, textStatus, errorThrown) {
				alert("权限不足");
			}
          })
}

$("#feng_mian").change(function () {
   var file_obj = $("#feng_mian")[0].files[0];
   var fd = new FormData();
   fd.append('img', file_obj);
   $.ajax({
       url: "/common/uploads/img/",
       type: "post",
       headers: {"X-CSRFToken": $.cookie("csrftoken")},
       data: fd,
       processData: false,
       contentType: false,
       success: function (res) {
           var obj = JSON.parse(res);
           $("#img").css('visibility','visible').attr('src',obj.data[0]);
       }
   })
});

$("#ch_feng_mian").change(function () {
   var file_obj = $("#ch_feng_mian")[0].files[0];
   var fd = new FormData();
   fd.append('img', file_obj);
   $.ajax({
       url: "/common/uploads/img/",
       type: "post",
       data: fd,
       headers: {"X-CSRFToken": $.cookie("csrftoken")},
       processData: false,
       contentType: false,
       success: function (res) {
           var obj = JSON.parse(res);
           $("#ch_feng_mian").parent().html('<img class="fm" id="ch_feng_mian_img" src="'+ obj.url +'">')
       }
   })
});

//添加文章到草稿箱
$(".to_draft").click(function () {
    var cur_url = "/admin/article_i/draft/";
    draft_or_audit(1, cur_url);
});

//添加文章到待审核
$(".to_audit").click(function () {
    var cur_url = "/admin/article_i/to_audit/";
    draft_or_audit(2, cur_url);
});


//已有的文章修改


//编辑页保存至待审核
$(".edit_audit").click(function () {
    var cur_id = $(this).attr("id_val");
    var cur_url = "/admin/article_i/to_audit/";
    draft_or_audit(2, cur_url=cur_url, cur_id=cur_id, reject_reason="")
});

//编辑页保存至草稿箱
$(".edit_draft").click(function () {
    var cur_id = $(this).attr("id_val");
    var cur_url = "/admin/article_i/draft/";
    draft_or_audit(1, cur_url=cur_url, cur_id=cur_id)
});

//保存至待发布
$(".edit_al_audit").click(function () {
    var cur_id = $(this).attr("id_val");
    var cur_url = "/admin/article_i/s_c/permit/";
    var jump_url = "/admin/article_i/to_audit/";
    status_change(3, cur_url=cur_url, cur_id=cur_id, jump_url=jump_url, reject_reason="")
});

//显示输入文本
$(".reject").mouseover(function () {
    $(".reject_reason").removeClass("not_display");
    $("#reject_reason").focus();
});

$(".reject").click(function () {
        var cur_id = $(this).attr("id_val");
        var reject_reason = $("#reject_reason").val();
        if (reject_reason == ""){
            alert("请输入驳回理由");
        }
        else {
            var cur_url = "/admin/article_i/s_c/reject/";
            var jump_url = "/admin/article_i/to_audit/";
            status_change(5, cur_url=cur_url, cur_id=cur_id, jump_url=jump_url, reject_reason=reject_reason)
        }
});

$("#reject_reason").keydown(function(e){
	 var e = e || event,
	 keycode = e.which || e.keyCode;
	 if (keycode == 13){
	     var cur_id = $(this).attr("id_val");
         var reject_reason = $(this).val();
         if (reject_reason == ""){
            alert("请输入驳回理由");
        }
        else {
            var cur_url = "/admin/article_i/s_c/reject/";
            var jump_url = "/admin/article_i/to_audit/";
            status_change(5, cur_url=cur_url, cur_id=cur_id, jump_url=jump_url, reject_reason=reject_reason)
        }
     }
})

$(".edit_back").mouseover(function () {
    $(".reject_reason").removeClass("not_display");
    $("#back_reason").focus();
});

$(".edit_publish").click(function () {
    var cur_id = $(this).attr("id_val");
    var cur_url = "/admin/article_i/s_c/publish/";
    var jump_url = "/admin/article_i/to_publish/";
    status_change(4, cur_url=cur_url, cur_id=cur_id, jump_url=jump_url, reject_reason="")
});

$(".edit_back").click(function () {
    var cur_id = $(this).attr("id_val");
    var reject_reason = $("#back_reason").val();
        if (reject_reason == ""){
            alert("请输入撤回理由");
        }
        else {
            var cur_url = "/admin/article_i/s_c/back/";
            var jump_url = "/admin/article_i/published/";
            status_change(1, cur_url=cur_url, cur_id=cur_id, jump_url=jump_url, reject_reason=reject_reason)
        }
});

$("#back_reason").keydown(function () {
     var e = e || event,
	 keycode = e.which || e.keyCode;
	 if (keycode==13) {
	    var cur_id = $(this).attr("id_val");
        var reject_reason = $(this).val();
        if (reject_reason == ""){
            alert("请输入撤回理由");
        }
        else {
            var cur_url = "/admin/article_i/s_c/back/";
            var jump_url = "/admin/article_i/published/";
            status_change(1, cur_url=cur_url, cur_id=cur_id, jump_url=jump_url, reject_reason=reject_reason)
        }
     }
});

$(".article_back").click(function () {
    var cur_url = window.location.href.split("?")[0];
    var cur_id = $(this).attr("id_val");
    $.ajax({
  			url: cur_url,
			type:'put',
            headers: {"X-CSRFToken": $.cookie("csrftoken")},
			dataType:'json',
            data:{
                id: cur_id,
                is_deleted: 0,
            },
			success:function(res){
				if(res.code=="200"){
				    alert("恢复成功");
			     	window.location.href = "/admin/recycle_bin/";
				}else{
					alert("权限不足");
				}
			},
			error : function(XMLHttpRequest, textStatus, errorThrown) {
				alert("权限不足");
			}
          })
});


$("input[name='add_in']").keydown(function(e){
	 var e = e || event,
	 keycode = e.which || e.keyCode;
	 if (keycode==13) {
	  	$(".log_btn").trigger("click");
		var name = $(this).val();
		if (name == ""){
			alert("不能为空");
			return
		}
		var url = $(this).attr("url");
		var cls = $(this).attr("cls");
		if (cls == "tag"){
		    var type = "checkbox";
        }
        else {
            var type = "radio";
        }
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
							$('.'+ cls +'s ').append('<span><input class="'+ cls +'" ' +
                                'type="'+ type +'" name="'+ cls +'" value="' + res.obj_id +
                                '" checked="checked">'+ name +'</span>')
                            $('input[name="add_in"]').val("");
						}else{
							alert(res.msg);
						}
					},
					error : function(XMLHttpRequest, textStatus, errorThrown) {
						alert("失败");
					}
				  })
 	}
});




