var qiniu_domain = "oa3cxbvmr.bkt.clouddn.com";

// Service type = "http" or "https" and so on
var service_type = "http";
var rpc_server = "http://localhost:8080";
var player_path = "/player.html";

function generate_qiniu_link(file_name) {
    "use strict";
    return service_type + "://" + qiniu_domain + "/" + file_name;
}

function getUrlParam(name) {
    "use strict";
    var reg = new RegExp("(^|&)" + name + "=([^&]*)(&|$)"), //构造一个含有目标参数的正则表达式对象
        r = window.location.search.substr(1).match(reg); //匹配目标参数
    if (r !== null) { return window.unescape(r[2]); } //返回参数值
}