$(".add_admin").click(function () {
   window.location.href = "/admin/add/";
});

$('input[type=radio][name=pos]').change(function() {
        if ($(this).prop("checked")) {
            var id = $(this).val();
            $.ajax({
                url: "/system/position/rights/?id=" + id,
                type: "get",
                headers: {"X-CSRFToken": $.cookie("csrftoken")},
                success: function (res) {
                    var json_res = $.parseJSON(res);
                    $("input[type='checkbox']").each(function () {
                        $(this).prop("checked", false);
                    });
                    $("input[name='right']").each(function () {
                        var result = $.inArray(parseInt($(this).val()), json_res.rights);
                        if (result != -1){
                            $(this).prop("checked", true);
                        }
                    });
                }
            })
        }
});

$(".group").click(function () {
    if ($(this).prop("checked")){
        $(this).parent().parent().next().children().children('input').prop("checked", true);
    }
    else {
        $(this).parent().parent().next().children().children('input').prop("checked", false);
    }
});

$(".right").click(function () {
    var allCheckNum = $(this).parent().siblings().children().length;
    var checkedNum = $(this).parent().siblings().children("input[type='checkbox']:checked").length;
    if ($(this).prop("checked")){
       if (allCheckNum == checkedNum){
           $(this).parent().parent().prev().children().children('input').prop("checked",true);
       }
   }
   else {
       {
           $(this).parent().parent().prev().children().children('input').prop("checked", false);
       }
   }
});

$(".submit_admin").click(function () {
   var name = $("#admin_name").val();
   var password = $("#password").val();
   var position_id = $("input[name='pos']:checked").val();
   var all_rights = []
    $("input[name='right']:checked").each(function () {
        all_rights.push($(this).val());
    });
   $.ajax({
       url: "/admin/",
       type: "post",
       headers: {"X-CSRFToken": $.cookie("csrftoken")},
       dataType: "json",
       data:{
           is_ajax: 1,
           name: name,
           position_id: position_id,
           password: password,
           rights: all_rights.toString(),
       },
       success: function (res) {
           if (res.code == "200"){
                alert(res.msg);
                window.location.href = "/admin/";
            }
            else {
                alert(res.msg)
            }
       }
   });
});

$(".submit_admin_ch").click(function () {
   var name = $("#admin_name").val();
   var password = $("#password").val();
   var position_id = $("input[name='pos']:checked").val();
   var id = $(this).attr("id_val");
   var all_rights = []
    $("input[name='right']:checked").each(function () {
        all_rights.push($(this).val());
    });
   $.ajax({
       url: "/admin/",
       type: "put",
       headers: {"X-CSRFToken": $.cookie("csrftoken")},
       dataType: "json",
       data:{
           id: id,
           name: name,
           position_id: position_id,
           password: password,
           rights: all_rights.toString(),
       },
       success: function (res) {
           if (res.code == "200"){
                alert(res.msg);
                window.location.href = "/admin/";
            }
            else {
                alert(res.msg)
            }
       },
   });
});