// jquery.js including required
// xmlrpc_lib.js including requeired
// config.js including required
// sub_group.js including requeire
// jquery.base64.js including required
// ABPlayerHTML5 including required

var loading_signal = {
    is_stop : true,
    pause_time : 500,
    target : {},
    create : function (interval, obj) {
        "use strict";
        this.pause_time = interval;
        this.target = obj;
        return this;
    },
    start : function () {
        "use strict";
        var t = this.target,
            self = this;
        this.is_stop = false;
        this.signal_1(this, this.pause_time);
    },
    stop : function () {
        "use strict";
        if (this.is_stop) { return; }
        this.is_stop = true;
    },
    done : function () {
        "use strict";
        if (this.is_stop) { return; }
        this.is_stop = true;
        this.target.innerHTML = "Done!";
    },
    failed : function () {
        "use strict";
        if (this.is_stop) { return; }
        this.is_stop = true;
        this.target.innerHTML = "Failed!";
    },
    signal_1 : function (self) {
        "use strict";
        if (self.is_stop) { return; }
        self.target.innerHTML = "-";
        setTimeout(function () { self.signal_2(self); }, self.pause_time);
    },
    signal_2 : function (self) {
        "use strict";
        if (self.is_stop) { return; }
        self.target.innerHTML = "\\";
        setTimeout(function () { self.signal_3(self); }, self.pause_time);
    },
    signal_3 : function (self) {
        "use strict";
        if (self.is_stop) { return; }
        self.target.innerHTML = "|";
        setTimeout(function () { self.signal_4(self); }, self.pause_time);
    },
    signal_4 : function (self) {
        "use strict";
        if (self.is_stop) { return; }
        self.target.innerHTML = "/";
        setTimeout(function () { self.signal_1(self); }, self.pause_time);
    }
};

var on_bangumi_episode_item_clicked = function (node, episode) {
    "use strict";
    var item = 0,
        i = 0,
        DOM_bangumi_list = document.getElementById("bangumi_list"),
        bangumi_name = "",
        current_bangumi = {},
        inst,
        src;
        
    bangumi_name = node.parentNode.previousSibling.innerHTML;
    for (item = 0; item < window.bangumis_list.length; item += 1) {
        if (window.bangumis_list[item].bangumi_name === bangumi_name) {
            current_bangumi = window.bangumis_list[item];
        }
    }
    window.$(node.parentNode.parentNode).append("<div id='player:" + bangumi_name + "' class='ABP-Unit' style='width:640px;height:480px;' tabindex='1'><div class='ABP-Video'><div class='ABP-Container'></div><video id='abp-video' autobuffer='false' data-setup='{}'><p>Your browser does not support html5 video!</p></video></div><div class='ABP-Text'><input type='text'></div><div class='ABP-Control'><div class='button ABP-Play'></div><div class='progress-bar'><div class='bar dark'></div><div class='bar'></div></div><div class='button ABP-CommentShow'></div><div class='button ABP-FullScreen'></div></div></div>");
    window.current_bangumi_info.info = current_bangumi.bangumi_episodes[episode];
    inst = window.ABP.bind(document.getElementById("player:" + bangumi_name), window.isMobile());
//    inst.txtText.focus();
    inst.txtText.addEventListener("keydown", function (e) {
        if (e && e.keyCode === 13) {
            if (/^!/.test(this.value)) { return; } //Leave the internal commands
            inst.txtText.value = "";
        }
    });
    window.abpinst = inst;
    window.current_bangumi_info.bangumi_name = window.current_bangumi_info.info.bangumi_name;
    window.current_bangumi_info.episode = episode;
    window.current_bangumi_info.video_url = window.current_bangumi_info.info.url;
    if (window.current_bangumi_info.video_url) {
        src = document.createElement("source");
        src.setAttribute("src", window.current_bangumi_info.video_url);
        src.setAttribute("type", "video/mp4");
        document.getElementById("player:" + bangumi_name).childNodes[0].childNodes[1].appendChild(src);
    }
    window.console.log(window.current_bangumi_info);
    window.danmaku_search(window.current_bangumi_info.bangumi_name, window.current_bangumi_info.episode);
};

var on_bangumi_item_clicked = function (node) {
    "use strict";
    var p = node.nextSibling,
        i = 0,
        item = 0,
        html_episodes = "",
        new_node = {},
        href;
    if (p.childNodes.length > 0) {     // collapse
        if (node.parentNode.childNodes[2]) {
            node.parentNode.removeChild(node.parentNode.childNodes[2]);
        }
        while (p.childNodes.length) {
            p.removeChild(p.childNodes[0]);
        }
    } else {
        for (item = 0; item < window.bangumis_list.length; item += 1) {
            if (window.bangumis_list[item].bangumi_name === node.innerHTML) {
                for (i in window.bangumis_list[item].bangumi_episodes) {
                    if (window.bangumis_list[item].bangumi_episodes.hasOwnProperty(i)) {
                        window.$(p).append("<a class='episode_item' onclick=on_bangumi_episode_item_clicked(this," + i + ")>[" + window.bangumis_list[item].bangumi_episodes[i].episode + "]</a>");
                    }
                }
            }
        }
    }
};

var generate_bangumi_list = function (array_bangumi) {
    "use strict";
    var ret_var = [],
        i = 0,
        k = 0,
        t = 0,
        collapse = false,
        episode = 0;
    for (i = 0; i < array_bangumi.length; i += 1) {
        collapse = false;
        episode = parseInt(array_bangumi[i].episode, 10);
        for (t = 0; t < k; t += 1) {
            if (ret_var[t].bangumi_name === array_bangumi[i].bangumi_name) {
                ret_var[t].bangumi_episodes[episode] = array_bangumi[i];
                collapse = true;
            }
        }
        if (!collapse) {
            ret_var[k] = {};
            ret_var[k].bangumi_episodes = [];
            ret_var[k].bangumi_name = array_bangumi[i].bangumi_name;
            ret_var[k].bangumi_episodes[episode] = array_bangumi[i];
            k += 1;
        }
    }
    return ret_var;
};

var rpc_get_file_list_callback = function (param) {
    "use strict";
    var item = 0,
        ret_obj = {},
        i = 0,
        bangumi_array = [],
        append_bangumi_item = "",
        temp_element = null,
        html_episodes = null;
    window.bangumis_list = {};
    if (param.errno !== 0) {
        window.console.log(param);
        window.first_loading_signal.failed();
        return;
    }
    window.first_loading_signal.done();
    ret_obj = window.jQuery.parseJSON(param.val.me);
    for (i =  0; i < ret_obj.length; i += 1) {
        bangumi_array[i] = window.bangumi_info.generate_bangumi_item_Qiniu(ret_obj[i]);
        bangumi_array[i].url = window.generate_qiniu_link(ret_obj[i].key); // generate URL
    }
    window.bangumis_list = generate_bangumi_list(bangumi_array);
    for (item = 0; item < window.bangumis_list.length; item += 1) {
        html_episodes = "<div class='bangumi_item' id='" + window.bangumis_list[item].bangumi_name + "'><li onclick=on_bangumi_item_clicked(this) >" + window.bangumis_list[item].bangumi_name + "</li>";
        html_episodes += "<div class='bangumi_episodes'></div></div>";
        window.$("#bangumi_list").append(html_episodes);
    }
};

var rpc_get_file_list_failed = function (e) {
    "use strict";
    window.first_loading_signal.failed();
    window.console.log(e);
};

var rpc_get_file_list = function () {
    "use strict";
    var client = new window.xmlrpc_client(window.rpc_server),
        msg = new window.xmlrpcmsg('list_files', []),
        resp = {};
    try {
        resp = client.send(msg, 20, rpc_get_file_list_callback);
    } catch (e) {
        rpc_get_file_list_failed(e);
    }
};

var main = function () {
    "use strict";
    window.first_loading_signal = loading_signal.create(150, document.getElementById("loading_signal"));
    window.first_loading_signal.start();
    window.rpc_get_file_list();
};
