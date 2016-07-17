var qiniu_domain = "oa3cxbvmr.bkt.clouddn.com";

// Service type = "http" or "https" and so on
var service_type = "http";
var rpc_server = "http://localhost:8080";

function generate_qiniu_link(file_name) {
    return service_type + "://" + qiniu_domain + "/" + file_name;
}
