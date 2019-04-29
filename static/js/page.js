$(".each_page").click(function () {
	var cur_url = window.location.href;
	var cur_page = $(this).text();
	if (cur_url.search(/&/) != -1){
		var jump_url = cur_url.split("?page=")[0] + "?page=" + cur_page + "&search=" +
			cur_url.split("&search=")[1];
	}
	else {
		var jump_url = cur_url.split("?page=")[0] + "?page=" + cur_page;
	}
	$("#content", parent.document.body).attr("src", jump_url);
});

$(".first").click(function () {
	var cur_url = window.location.href;
	if (cur_url.search(/&/) != -1){
		var jump_url = cur_url.split("?page=")[0] + "?page=" + 1 + "&search=" +
			cur_url.split("&search=")[1];
	}
	else {
		var jump_url = cur_url.split("?page=")[0] + "?page=" + 1;
	}
	$("#content", parent.document.body).attr("src", jump_url);
});

$(".end").click(function () {
	var cur_url = window.location.href;
	var end = parseInt($(this).attr("end"));
	if (cur_url.search(/&/) != -1){
		var jump_url = cur_url.split("?page=")[0] + "?page=" + end + "&search=" +
			cur_url.split("&search=")[1];
	}
	else {
		var jump_url = cur_url.split("?page=")[0] + "?page=" + end;
	}
	$("#content", parent.document.body).attr("src", jump_url);
});

$(".last").click(function () {
	var cur_url = window.location.href;
	var last = $(this).attr("cur_page") - 1;
	if (last <= 0){
		last = 1;
	}
	if (cur_url.search(/&/) != -1){
		var jump_url = cur_url.split("?page=")[0] + "?page=" + last + "&search=" +
			cur_url.split("&search=")[1];
	}
	else {
		var jump_url = cur_url.split("?page=")[0] + "?page=" + last;
	}
	$("#content", parent.document.body).attr("src", jump_url);
});

$(".next").click(function () {
	var cur_url = window.location.href;
	var next = parseInt($(this).attr("cur_page")) + 1;
	if (next >= parseInt($(this).attr("end"))){
		next = parseInt($(this).attr("end"));
	}
	if (cur_url.search(/&/) != -1){
		var jump_url = cur_url.split("?page=")[0] + "?page=" + next + "&search=" +
			cur_url.split("&search=")[1];
	}
	else {
		var jump_url = cur_url.split("?page=")[0] + "?page=" + next;
	}
	$("#content", parent.document.body).attr("src", jump_url);
});