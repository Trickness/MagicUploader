# coding=utf8

from qiniu import Auth, put_file, etag, urlsafe_base64_encode
from qiniu import BucketManager
from FileStatus import FileStatus
import time
from xmlrpc.client import ServerProxy
from json import encoder, decoder
import json
from MUConfig import MagicUploaderConfig


def upload_process(uploaded_size: int, file_size: int):
    print("%d of %d" % (uploaded_size, file_size))

class QiniuUploader:
    __is_initialized = False
    __access_key = ""
    __secret_key = ""
    __bucket_name = ""

    def __init__(self):
        pass

    def set_auth(self, access_key: str, secret_key: str, bucket_name: str):
        self.__access_key = access_key
        self.__secret_key = secret_key
        self.__bucket_name = bucket_name
        self.__auth = Auth(self.__access_key, self.__secret_key)
        self.__bucket = BucketManager(self.__auth)
        self.__is_initialized = True
        return True

    def upload(self, file_from: str, file_to: str, process_callback):
        if not self.__is_initialized:
            print("Have not been initialized!")
            return None
        print("Qiniu Ready Upload [%s]" % file_from)
        token = self.__auth.upload_token(self.__bucket_name, file_to)
        ret, info = put_file(token, file_to, file_from, progress_handler=process_callback)
        assert ret['key'] == file_to
        assert ret['hash'] == etag(file_from)
        return info

    def remove(self, file_name):
        if not self.__is_initialized:
            print("Have not been initialized!")
            return None
        ret, info = self.__bucket.delete(self.__bucket_name, file_name)
        return info

    def list_files(self) -> list:
        ret = self.__bucket.list(self.__bucket_name)
        if ret[2].status_code != 200:
            return ret
        return_var = []
        for item in ret[0]['items']:
            assert isinstance(item, dict)
            return_var.append(item)
        return return_var


class Uploader:
    __type = -1
    TYPE_QINIU = 0
    __uploaders = [QiniuUploader()]
    __do_upload = True
    __upload_hidden_file = False
    __show_process = False
    __process_callback = None

    def _init__(self):
        pass

    def _init_qiniu(self, bucket_name=MagicUploaderConfig.Qiniu_bucket_name,
                    access_key=MagicUploaderConfig.Qiniu_access_key,
                    secret_key=MagicUploaderConfig.Qiniu_secret_key):
        if (self.__uploaders[self.TYPE_QINIU].set_auth(access_key, secret_key, bucket_name)):
            self.__type = self.TYPE_QINIU

    def _set_do_upload(self, do_upload: bool):
        self.__do_upload = do_upload

    def _set_upload_hidden_file(self, upload_hidden_file: bool):
        self.__upload_hidden_file = upload_hidden_file

    def _set_show_process(self, show_process: bool, process_callback=upload_process):
        self.__show_process = show_process
        self.__process_callback = process_callback

    def _upload(self, file_from: str, file_to: str):
        if not self.__do_upload:
            print("[Settings] : Dont upload")
            return
        if file_from[2] == '.':
            if not self.__upload_hidden_file:
                return
        while (1):
            try:
                fs = FileStatus(file_from)
            except OSError as e:
                print("OS Error file[%s]" % e.filename)
                return
            if fs.status()['is_opened']:
                time.sleep(5)
                continue
            break
        process_handler = None
        if self.__show_process:
            if callable(self.__process_callback):
                process_handler = self.__process_callback
        try:
            info = self.__uploaders[self.__type].upload(file_from, file_to, process_handler)
        except IndexError as e:
            print("You must initilize a uploader before use")
            return
        print(info)

    def _remove(self, file_name: str):
        if not self.__do_upload:
            print("[Settings] : Dont remove")
            return
        try:
            self.__uploaders[self.__type].remove(file_name)
        except IndexError as e:
            print("You must initilize a uploader before use")

    def list_files(self):
        print("Entry!")
        try:
            var = self.__uploaders[self.__type].list_files()
        except IndexError as e:
            print("You must initilize a uploader before use")
        return json.dumps(var)

    def _dispatch(self, method, params):
        return 'bad method'
