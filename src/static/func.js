function dhl_on_jiaodian(yuansu) {
	// var Change = document.get
	yuansu.style.backgroundColor = 'rgb(124,124,124)' ;
}


function dhl_on_likai(yuansu) {
	
	yuansu.style.backgroundColor = 'darkgray' ;
	
}

function dhl_jump_page(target) {
	
	window.location.href = target;
	
}

var gb_highfunc_show_status = 0;

function show_hid_gb_devfunc(){

	if (gb_highfunc_show_status==0) {

		highfunc_btns.style.display = "block";
		gb_highfunc_show_status=1;

	}else{

		highfunc_btns.style.display = "none";
		gb_highfunc_show_status=0;

	}


}

var gb_show_status=0;

function show_hid_how_use() {

	var textp = document.getElementById("how2_use");
	if (gb_show_status==0) {

		// window.alert("成功弹出警告框！");

		textp.innerHTML = "<hr>在使用前请先使用解锁键盘锁&删除控制锁定软件功能<br/>点击替换拦截程序后再恢复控屏软件<br/>等待老师控制屏幕后即完成拦截远程命令<br/>完成替换后即可重新删除控屏软件<br/>此时当老师处于控制状态时你可以主动运行命令弹出窗口化共享屏幕<br/>实现自由的同时不影响听课!!<br/>当老师来时你可以使用快捷键启动全屏参数的控制<br/>等待老师走后再用快捷键清理进程<hr>";
		gb_show_status = 1;
	} else {

		textp.innerHTML = "";
		gb_show_status = 0;

	}

}




function doget_use_func(target) {
	var url = '//127.0.0.1:22330/func/' + target;

	fetch(url)
	// .then(location.reload());
	.then(window.setTimeout(function () {window.location.reload();},1000));
	// 等待1S再刷新
	// 不然老机器会丢弃请求我是真无语到了
	
}

function use_func_wait_time(target,time) {
	var url = '//127.0.0.1:22330/func/' + target;
	console.log("Wait Reflash time > ",time)

	fetch(url)
	// .then(location.reload());
	// .then(window.setTimeout(function () {window.location.reload();},1000));

	.then(window.setTimeout(function () {window.location.reload();},time));
	// 等待1S再刷新
	// 不然老机器会丢弃请求我是真无语到了
	
}

function doget_use_func_with_wait(target) {
	var url = '//127.0.0.1:22330/func/' + target;
	// alert('123');
	// var url = loc ;
	// console.log(loc);
	// console.log(url);
	// $.get(url);
	fetch(url)
	// .then(location.reload())
	.then(window.setTimeout(function () {window.location.reload();},2000));
	// 等待2再刷新
	
}

function doget_use_normal(target) {
	var url = '//127.0.0.1:22330/' + target;
	// alert('123');
	// var url = loc ;
	// console.log(loc);
	// console.log(url);
	// $.get(url);
	fetch(url);
	// .then(location.reload())
	// .catch(location.reload())
	
}