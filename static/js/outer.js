$(".second_level").eq(0).css({"display": "block"});
$(".first_level").hover(function () {
   $(this).css({"color":"#2e6da4"});
}, function () {
    $(this).css({"color": "black"})
});
$(".second_level li span").hover(function () {
   $(this).css({"color":"#2e6da4"});
}, function () {
    $(this).css({"color": "black"})
});
$(".first_level").click(function(){
    if ($(this).hasClass("glyphicon-chevron-down")){
        $(this).removeClass("glyphicon-chevron-down").addClass("glyphicon-chevron-right").removeClass("current")
            .next("div.second_level").slideUp("slow");
    }
    else {
    $(this).addClass("current").removeClass("glyphicon-chevron-right")
        .addClass("glyphicon-chevron-down").next("div.second_level").slideToggle(300).siblings("div.second_level")
        .slideUp("slow");
    $(this).siblings().removeClass("current").removeClass("glyphicon-chevron-down").addClass("glyphicon-chevron-right")
    }
});

//iframe获取父级内容
$(".second_level span").click(function () {
    var url = $(this).attr("href");
    $(this).parent().siblings().removeClass("red_font");
    $(this).siblings().removeClass("red_font");
    $(this).addClass("red_font");
    $("#content", parent.document.body).attr("src", url)

});
$(".delete_obj").click(function () {
    alert($(this).attr("obj_id"));
});
$(".detail").click(function () {
    var cur_url = window.location.href;
    var cur_id = $(this).attr("id_val");
    window.location.href = cur_url + "?id=" + cur_id;
})