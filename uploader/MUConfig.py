# coding=utf8


class MagicUploaderConfig:
    Qiniu_access_key = "vvDreC5B-FSzDuDmRIDdXY1nyqhIz7xJ3qC9iOjB"
    Qiniu_secret_key = "Qkw1gSYBvxD2_I08dq4GIm0JQmUDaXfsLw-9gGu8"
    Qiniu_bucket_name= "resources"

    dont_upload = [".*\.aria2$",".*__temp.*",".*__pycache__.*",".*tmp__.*", ".*\.torrent$"]

    root_path = "/home/tricks/Downloads"
