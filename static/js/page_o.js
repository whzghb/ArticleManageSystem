$(".each_page").click(function () {
	var cur_url = window.location.href;
	var cur_page = $(this).text();
	var jump_url = cur_url.split("?page=")[0] + "?page=" + cur_page;
	window.location.href = jump_url;
});

$(".first").click(function () {
	var cur_url = window.location.href;
	var jump_url = cur_url.split("?page=")[0] + "?page=" + 1;
	window.location.href = jump_url;
});

$(".end").click(function () {
	var cur_url = window.location.href;
	var end = parseInt($(this).attr("end"));
	var jump_url = cur_url.split("?page=")[0] + "?page=" + end;
	window.location.href = jump_url;
});

$(".last").click(function () {
	var cur_url = window.location.href;
	var last = $(this).attr("cur_page") - 1;
	if (last <= 0){
		last = 1;
	}
	var jump_url = cur_url.split("?page=")[0] + "?page=" + last;
	window.location.href = jump_url;
});

$(".next").click(function () {
	var cur_url = window.location.href;
	var next = parseInt($(this).attr("cur_page")) + 1;
	if (next >= parseInt($(this).attr("end"))){
		next = parseInt($(this).attr("end"));
	}
	var jump_url = cur_url.split("?page=")[0] + "?page=" + next;
	window.location.href = jump_url;
});