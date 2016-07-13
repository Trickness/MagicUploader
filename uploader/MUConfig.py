# coding=utf8


class MagicUploaderConfig:
    Qiniu_access_key = ""
    Qiniu_secret_key = ""
    Qiniu_bucket_name= ""

    dont_upload = [".*\.aria2$",".*__temp.*",".*__pycache__.*",".*tmp__.*"]

    root_path = "../../../"
