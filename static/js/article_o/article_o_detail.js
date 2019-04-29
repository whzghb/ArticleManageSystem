function zan(view, id, ths, cls) {
    var url = "/article/zan/"
    $.ajax({
        url: url,
        type: "post",
        headers: {"X-CSRFToken": $.cookie("csrftoken")},
        dataType: 'json',
        data: {
            id: id,
            view: view,
        },
        success: function (res) {
            if (res.code != '403'){
                if (cls == "good") {
                    if (res.is_view == 1) {
                        $('.tip').addClass('alert-warning').html('已经评价过').show().delay(1000).fadeOut();
                    }
                    else {
                        $(ths).next().text('(' + res.good_view.toString() + ')');
                        $(ths).next().next().next().text('(' + res.bad_view.toString() + ')');
                    }
                }
                else {
                    if (res.is_view == 1) {
                        $('.tip').addClass('alert-warning').html('已经评价过').show().delay(1000).fadeOut();
                    }
                    else {
                        $(ths).next().text('(' + res.bad_view.toString() + ')');
                        $(ths).prev().text('(' + res.good_view.toString() + ')');
                    }
                }
            }
            else {
                $(".hid").removeClass("no_display");
                $(".log").removeClass("no_display");
                $("body").addClass("tanceng");
            }
        },
        error: function (XMLHttpRequest, textStatus, errorThrown) {
            alert("异常");
        }
    })
};


function comment(id, content, parent_id, ths) {
    var url = "/article/comment/"
    $.ajax({
        url: url,
        type: "post",
        headers: {"X-CSRFToken": $.cookie("csrftoken")},
        dataType: 'json',
        data: {
            id: id,
            content: content,
            parent_id: parent_id,
        },
        success: function (res) {
            if (res.code != 403) {
                window.location.reload();
            }
            else {
                 $(".hid").removeClass("no_display");
                 $(".log").removeClass("no_display");
                 $("body").addClass("tanceng");
            }
        },
        error: function (XMLHttpRequest, textStatus, errorThrown) {
            // $(".hid").removeClass("no_display");
            // $(".log").removeClass("no_display");
            // $("body").addClass("tanceng");
            alert("异常");
        }
    })
};

$(".click_say_back").click(function () {
    $(this).parent().siblings().children("div").addClass("no_display");
    $(this).next().removeClass("no_display");
    $(this).next().children("textarea").focus();
});

$(".submit_back").click(function () {
    var content = $(this).prev().val();
    if (content == ""){
            alert("请输入内容");
            return
        }
    var id = $(this).attr("article_id");
    var parent_id = $(this).attr("id_val");
    comment(id, content, parent_id, this)
});

$(".good").click(function () {
    var id = $(this).attr("id_val");
    zan(1, id, this, "good");
});

$(".bad_c").click(function () {
    var id = $(this).attr("id_val");
    zan(2, id, this, "bad");
});

$(".submit_comment").click(function () {
    var id = $(this).attr("id_val");
    var content = $(this).prev().val();
    if (content == ""){
            alert("请输入内容");
            return
        }
    var parent_id = null;
    comment(id, content, parent_id, this);
});

$("textarea[name='comment']").keydown(function (e) {
    var e = e || event,
        keycode = e.which || e.keyCode;
    if (keycode == 13) {
        $(".log_btn").trigger("click");
        var id = $(this).next().attr("id_val");
        var content = $(this).val();
        if (content == ""){
            alert("请输入内容");
            return
        }
        var parent_id = null;
        comment(id, content, parent_id, this);
    }
});

$(".say_back").keydown(function (e) {
    var e = e || event,
        keycode = e.which || e.keyCode;
    if (keycode == 13) {
        $(".log_btn").trigger("click");
        var content = $(this).val();
        if (content == ""){
            alert("请输入内容");
            return
        }
        var id = $(this).next().attr("article_id");
        var parent_id = $(this).next().attr("id_val");
        comment(id, content, parent_id, this)
    }
});

$(".login").click(function () {
    var name = $("#name2").val();
    var password = $("#password2").val();
    var url = "/user/login/"
    if (name == "") {
        alert("请输入用户名");
    }
    else if (password == "") {
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
                    if (name.indexOf("\\u") > 0) {
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
                    $(".user").html('<span id="user">' + str + '</span>&nbsp;|&nbsp;<span><a href="/user/logout/">注销</a></span>');
                    $(".hid").addClass("no_display");
                    $(".outer2").addClass("no_display");
                    $("body").removeClass("tanceng");
                    // window.location.reload();
                } else {
                    $("#name2").val(name);
                    $("#password2").val(password);
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

$("#password2").keydown(function () {
    var e = e || event,
        keycode = e.which || e.keyCode;
    if (keycode == 13) {
        var name = $("#name2").val();
        var password = $("#password2").val();
        var url = "/user/login/"
        if (name == "") {
            alert("请输入用户名");
        }
        else if (password == "") {
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
                        if (name.indexOf("\\u") > 0) {
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
                        $(".user").html('<span id="user">' + str + '</span>&nbsp;|&nbsp;<span><a href="/user/logout/">注销</a></span>');
                        $(".hid").addClass("no_display");
                        $(".outer2").addClass("no_display");
                        $("body").removeClass("tanceng");
                        // window.location.reload();
                    } else {
                        $("#name2").val(name);
                        $("#password2").val(password);
                        alert(res.error);
                    }
                },
                error: function (XMLHttpRequest, textStatus, errorThrown) {
                    alert("失败");
                }
            })
        }
    }
});

$(".register").click(function () {
    var name = $("#name3").val();
    var password = $("#password3").val();
    var re_password = $("#re_password3").val();
    var url = "/user/register/"
    if (name == "") {
        alert("请输入用户名");
    }
    else if (password == "") {
        alert("请输入密码");
    }
    else if (re_password == "") {
        alert("请确认密码");
    }
    else if (password != re_password) {
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
                    $(".reg").addClass("no_display");
                    $(".log").removeClass("no_display");
                    $("#name2").val(name);
                    $("#password2").val(password);
                    // window.location.reload();
                } else {
                    $("#name3").val(name);
                    $("#password3").val(password);
                    $("#re_password3").val(re_password);
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

$("#re_password3").keydown(function () {
    var e = e || event,
        keycode = e.which || e.keyCode;
    if (keycode == 13) {
        var name = $("#name3").val();
        var password = $("#password3").val();
        var re_password = $("#re_password3").val();
        var url = "/user/register/"
        if (name == "") {
            alert("请输入用户名");
        }
        else if (password == "") {
            alert("请输入密码");
        }
        else if (re_password == "") {
            alert("请确认密码");
        }
        else if (password != re_password) {
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
                        $(".reg").addClass("no_display");
                        $(".log").removeClass("no_display");
                        $("#name2").val(name);
                        $("#password2").val(password);

                    } else {
                        $("#name3").val(name);
                        $("#password3").val(password);
                        $("#re_password3").val(re_password);
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

$(".undo").click(function () {
    $(".hid").addClass("no_display");
    $(".outer2").addClass("no_display");
    $("*").removeClass("tanceng");
});

$(".reg_cli").click(function () {
    $(".outer2").addClass("no_display");
    $(".reg").removeClass("no_display");
    $(".body").removeClass("tanceng");
});

$(".say_back").blur(function () {
    $(this).parent().addClass("no_display");
});

$(".del_com").click(function () {
   var id = $(this).attr("id_val");
   $.ajax({
       url: "/common/comment/user_del/?id=" + id,
       type: "get",
       success: function () {
           $(this).text('已删除');
           $(this).removeClass("del_com").removeClass("cursor").addClass("del_com_sty");
           $(this).next().find('span:first').addClass("bad").text("该评论已删除");
       }.bind(this)
   })
});

$(function () {
    var user_name = $.cookie("user_name");
    if (user_name == null){
        user_name = ""
    }
    else {
        var str = "";
        if (user_name.indexOf("\\u")>0) {
            var str = "";
            var s = user_name.split('\\u');
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
            str = user_name.replace('"', '').replace('"', '');
        }
        user_name = str + ":"
    }
   $("#comm_to_art").attr("placeholder", user_name.replace(" ", "").replace("\t", ""));
});
