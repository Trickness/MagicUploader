// jquery.js including required
// xmlrpc_lib.js including requeired
// config.js including required
// sub_group.js including requeire

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

var rpc_get_file_list_callback = function (param) {
    "use strict";
    var item = 0,
        ret_obj = {},
        i = 0,
        bangumi_array = [],
        append_bangumi_item = "",
        temp_element = null;
    if (param.errno !== 0) {
        window.console.log(param);
        window.first_loading_signal.failed();
        return;
    }
    window.first_loading_signal.done();
    window.console.debug(window.jQuery.parseJSON(param.val.me));
    ret_obj = window.jQuery.parseJSON(param.val.me);
    for (i =  0; i < ret_obj.length; i += 1) {
        bangumi_array[i] = window.bangumi_info.generate_bangumi_item_Qiniu(ret_obj[i]);
    }
    window.$("#bangumi_list").append("<ol>");
    for (item = 0; item < ret_obj.length; item += 1) {
        bangumi_array[item].url = window.generate_qiniu_link(ret_obj[item].key); // generate URL
        temp_element = document.getElementById(bangumi_array[item]);
        if (temp_element !== null) {
            append_bangumi_item = " <a href='" + bangumi_array[item].url + "'>[" + bangumi_array[item].episodes + "]</a>";
        } else {
            append_bangumi_item = "<li class='bangumi_item' " + "id='" + bangumi_array[item].bangumi_name + "'>" + bangumi_array[item].bangumi_name + " <a href='" + bangumi_array[item].url + "'>[" + bangumi_array[item].episodes + "]</a></li>";
        }
        window.$("#bangumi_list").append(append_bangumi_item);
        window.console.log(append_bangumi_item);
    }
    window.$("#bangumi_list").append("</ol>");
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
    //client.setDebug(2);
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