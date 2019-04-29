$(".del_com").click(function () {
   var id = $(this).attr("id_val");
   $.ajax({
       url: "/common/comment/admin_del/",
       type: "post",
       headers: {"X-CSRFToken": $.cookie("csrftoken")},
       data:{
           id: id,
       },
       success: function (res) {
           var rlt = $.parseJSON(res);
           if (rlt.code != "403")
           {
               if ($(this).text() == "删除"){
                   $(this).text('恢复');
               }
               else {
                   $(this).text('删除');
               }
           }
           else {
               alert(rlt.msg);
           }
           // $(this).removeClass("del").removeClass("cursor");
           // window.location.reload();
       }.bind(this)
   })
});