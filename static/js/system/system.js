$(".add_pos").click(function () {
   window.location.href = "/system/position/add/";
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

$(".submit_pos").click(function () {
    var all_rights = []
    $("input[name='right']:checked").each(function () {
        all_rights.push($(this).val());
    });
    var name = $("#pos_name").val();
    $.ajax({
        url: "/system/position/",
        type: "post",
        headers: {"X-CSRFToken": $.cookie("csrftoken")},
        dataType: "json",
        data:{
            is_ajax: 1,
            name: name,
            rights: all_rights.toString(),
        },
        success:function (res) {
            if (res.code == "200"){
                alert(res.msg);
                window.location.href = "/system/position/";
            }
            else {
                alert(res.msg)
            }
        },
    });
});

$(".submit_pos_ch").click(function () {
    var all_rights = []
    $("input[name='right']:checked").each(function () {
        all_rights.push($(this).val());
    });
    var name = $("#pos_name").val();
    var id = $(this).attr("id_val");
    $.ajax({
        url: "/system/position/",
        type: "put",
        dataType: "json",
        headers: {"X-CSRFToken": $.cookie("csrftoken")},
        data:{
            is_ajax: 1,
            id: id,
            name: name,
            rights: all_rights.toString(),
        },
        success:function (res) {
            if (res.code == "200"){
                alert(res.msg);
                window.location.href = "/system/position/";
            }
            else {
                alert(res.msg)
            }
        },
    });
});
