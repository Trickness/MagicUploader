var bangumi_info = {
    is_normal_format  : function (filename) {
        "use strict";
        var re = /.+?\[/g;
        if (re.test(filename)) {
            re = /.*\.mp4$/g;
            return re.test(filename);
        }
        return false;
    },
    get_content : function (str) {
        "use strict";
        return str.substring(1, str.length - 1);
    },
    anaylise_filename : function (filename) {
        "use strict";
        var re = /\[.+?\]/g,
            ret = {
                publisher_name  : "",
                bangumi_name    : "",
                episode         : "0",
                is_end          : false,
                is_bd           : false,
                resolution      : "1280x720",    // 720P
                file_hash       : "",
                file_type       : "video/mp4",
                file_size       : 0,
                upload_time     : 0,
                url             : "",
                subs            : {
                    has_sub         : true,
                    sub_group_name  : "",
                    is_embeded      : true,
                    language        : "Simplified Chinese"  // [Simplified Chinese] , [Traditional Chinese] , [English], [other(minxed)]
                },
                comments        : [
                    
                ]
            },
            var_array   = filename.match(re),
            i           = 0,
            temp_var    = "";
        // publisher name
        ret.publisher_name = this.get_content(re.exec(filename)[0]);
        ret.subs.sub_group_name = ret.publisher_name;
        
        if (!this.is_normal_format(filename)) {
            return "resource";
        }
        
        ret.bangumi_name    = this.get_content(var_array[1]).replace(/_/g, ' ');
        ret.episode        = this.get_content(var_array[2]);
        
        for (i = 3; i < var_array.length; i += 1) {
            temp_var = this.get_content(var_array[i]).toLocaleUpperCase();
            if (temp_var === "END") {
                ret.is_end = true;
            } else if (temp_var === "BDRIP") {
                ret.is_bd = true;
            } else if (temp_var === "1080P") {
                ret.resolution = "1920x1080";
            } else if (temp_var === "720P") {
                ret.resolution = "1280x720";
            } else if (temp_var === "1280X720") {
                ret.resolution = "1280x720";
            } else if (temp_var === "1920X1080") {
                ret.resolution = "1920x1080";
            } else if (temp_var === "BIG5") {
                ret.subs.has_sub = true;
                ret.subs.is_embeded = true;
                ret.subs.language = "Traditional Chinese";
            } else if (temp_var === "CHT") {
                ret.subs.has_sub = true;
                ret.subs.is_embeded = true;
                ret.subs.language = "Traditional Chinese";
            } else if (temp_var === "CHS") {
                ret.subs.has_sub = true;
                ret.subs.is_embeded = true;
                ret.subs.language = "Simplified Chinese";
            } else if (temp_var === "GB") {
                ret.subs.has_sub = true;
                ret.subs.is_embeded = true;
                ret.subs.language = "Simplified Chinese";
            }
        }
        return ret;
    },
    generate_bangumi_item_Qiniu : function (info) {
        "use strict";
        var ret_var = this.anaylise_filename(info.key);
        if (ret_var === "resource") {
            return "resource";
        }
        ret_var.file_hash   = info.hash;
        ret_var.file_type   = info.mimeType;
        ret_var.upload_time = info.putTime;
        ret_var.file_size   = info.fsize;
        
        return ret_var;
    }
};
