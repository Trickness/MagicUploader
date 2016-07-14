var qiniu_domain = "";

// Service type = "http" or "https" and so on
var service_type = "http";

function generate_qiniu_link(file_name) {
    return service_type + "://" + qiniu_domain + "/" + file_name;
}
