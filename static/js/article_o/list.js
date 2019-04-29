var cur_page = 1;

$(".get_more").click(function () {
    var cur_url = window.location.href;
    var next_page = cur_page + 1;
    cur_page = next_page;
    var next_url = cur_url + "?page=" + next_page;
    $.ajax({
        url: next_url,
        type: "get",
        headers: {"X-CSRFToken": $.cookie("csrftoken")},
        success: function (res) {
            if (res.data.length == 0) {
                $('.get_more').text("没有更多了");
                return
            }
            $.each(res.data, function (i, item) {
                $('.container').append(
                    '<div class="each_art">' +
                    '<hr style="clear: left; visibility: hidden"><div class="img"><img src=' + item.img + '>' +
                    '</div>' +
                    '<div class="info">' +
                    '<div class="art_title" id_val="' + item.id + '">' +
                    '<a href="/article/?id=' + item.id + '" target="_blank">' + item.title + '</a>' +
                    '</div>' +
                    '<div class="art_oth">' +
                    '<span class="author">' + item.author + '</span>' +
                    '<span class="time">' + item.pub_time.replace("T", " ") + '</span>' +
                    '</div>' +
                    '</div><hr style="clear: left">'
                )
            });
        },
        error: function (XMLHttpRequest, textStatus, errorThrown) {
            alert("异常");
        }
    })
});

$(window).scroll(function () {
    var scrollTop = $(this).scrollTop();
    var scrollHeight = $(document).height();
    var windowHeight = $(this).height();
    if (scrollTop + windowHeight == scrollHeight) {
        $('.get_more').text("正在加载...");
        setTimeout(function () {
            var cur_url = window.location.href;
            var next_page = cur_page + 1;
            cur_page = next_page;
            var next_url = cur_url + "?page=" + next_page;
            $.ajax({
                url: next_url,
                type: "get",
                headers: {"X-CSRFToken": $.cookie("csrftoken")},
                success: function (res) {
                    if (res.data.length == 0) {
                        $('.get_more').text("没有更多了");
                        return
                    }
                    $.each(res.data, function (i, item) {
                        $('.container').append(
                            '<div class="each_art">' +
                            '<hr style="clear: left; visibility: hidden"><div class="img"><img src=' + item.img + '>' +
                            '</div>' +
                            '<div class="info">' +
                            '<div class="art_title" id_val="' + item.id + '">' +
                            '<a href="/article/?id=' + item.id + '" target="_blank">' + item.title + '</a>' +
                            '</div>' +
                            '<div class="art_oth">' +
                            '<span class="author">' + item.author + '</span>' +
                            '<span class="time">' + item.pub_time.replace("T", " ") + '</span>' +
                            '</div>' +
                            '</div><hr style="clear: left">'
                        )
                    });
                    $('.get_more').text("加载更多");
                },
                error: function (XMLHttpRequest, textStatus, errorThrown) {
                    alert("异常");
                }
            })
        }, 600)
    }
});