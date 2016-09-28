var qiniu_domain = "oa3cxbvmr.bkt.clouddn.com";

// Service type = "http" or "https" and so on
var service_type = "http";
var rpc_server = "http://localhost.moe:8080";

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

window.current_bangumi_info =  {
    bangumi_name : "",
    type : 0,       // 1  - TV动画
                    // 2  - TV动画特别放送
                    // 3  - OVA
                    // 4  - 剧场版
                    // 5  - 音乐视频（MV）
                    // 6  - 网络放送
                    // 7  - 其他分类
                    // 10 - 三次元电影
                    // 20 - 三次元电视剧或国产动画
                    // 99- 未知（尚未分类）
    episode : 0,
    episode_id : 0,
    episode_title : "",
    video_url : "",
    info : {}
};

window.http_request = new XMLHttpRequest();
var search_DandanPlay_danmaku_callback = function (param) {
    "use strict";
    var response,
        i,
        url;
    if (param.currentTarget.readyState === 4 && param.currentTarget.status === 200) {
        i = 0;
        response = window.jQuery.parseJSON(param.currentTarget.responseText);
        window.console.log(response);
        for (i in response.Animes) {
            if (response.Animes.hasOwnProperty(i)) {
                window.current_bangumi_info.bangumi_name = response.Animes[i].Title;
                window.current_bangumi_info.episode_id = response.Animes[i].Episodes[0].Id;
                window.current_bangumi_info.episode_title = response.Animes[i].Episodes[0].Title;
                window.current_bangumi_info.type = response.Animes[i].Type;
            }
        }
        url = "http://acplay.net/api/v1/comment/" + window.current_bangumi_info.episode_id + "?from=0";
        window.http_request.onreadystatechange = get_DandanPlay_danmaku_callback;
        window.http_request.open("GET",url);
        window.http_request.send();


        //(new window.CommentLoader(window.abpinst.cmManager)).setParser(window.DandanplayParser).load('GET', url);
    }
};

var get_DandanPlay_danmaku_callback = function (param) {
    "use strict"
    var response,
        i,
        JSONValues;
    if (param.currentTarget.readyState === 4 && param.currentTarget.status === 200) {
        JSONValues = response = window.jQuery.parseJSON(param.currentTarget.responseText);
        window.console.log(JSONValues);
        var url = "http://acplay.net/api/v1/comment/" + window.current_bangumi_info.episode_id + "?from=0";

        //(new window.CommentLoader(window.abpinst.cmManager)).setParser(window.DandanplayParser).load('GET', url);
        var danmaku_list = window.$("#danmaku");
        for (i in JSONValues.Comments){
            danmaku_list.append("<p>" + JSONValues.Comments[i].Time + " : " + JSONValues.Comments[i].Message + "</p>");
            window.console.log(JSONValues.Comments[i]);
        }
        (new window.CommentLoader(window.abpinst.cmManager)).setParser(window.DandanplayParser).load('GET', "http://acplay.net/api/v1/comment/" + window.current_bangumi_info.episode_id + "?from=0");

    }
}

var danmaku_search = function (bangumi_name, bangumi_episode, danmaku_provider) {
    "use strict";
    if (danmaku_provider === "DandanPlay") {
        window.http_request.onreadystatechange = search_DandanPlay_danmaku_callback;
        window.http_request.open("GET", "http://acplay.net/api/v1/searchall/"  + encodeURIComponent(bangumi_name) + "/" + bangumi_episode);
        window.http_request.send();
    }
    return null;
    
};
