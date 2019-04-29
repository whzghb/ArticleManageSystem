$(".edit").click(function () {
    var cur_url = window.location.href;
    var id = $(this).attr("id_val");
    var cur_url = cur_url.split("admin")[0] + "admin/article_i/edit/?id=" + id;
    window.location.href = cur_url;
})