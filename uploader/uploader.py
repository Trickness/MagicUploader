# coding=utf8

from qiniu import Auth, put_file, etag, urlsafe_base64_encode
from qiniu import BucketManager
import qiniu.config
from xmlrpc.server import SimpleXMLRPCServer


class QiniuUploader:
    __is_initialized = False
    __access_key = ""
    __secret_key = ""
    __bucket_name = ""
    def __init__(self):
        pass
    def setAuth(self, access_key : str, secret_key : str, bucket_name : str):
        self.__access_key = access_key
        self.__secret_key = secret_key
        self.__bucket_name = bucket_name
        self.__auth = Auth(self.__access_key, self.__secret_key)
        self.__bucket = BucketManager(self.__auth)
        self.__is_initialized = True

    def upload(self, file_from: str, file_to: str):
        if not self.__is_initialized:
            print ("Have not been initialized!")
            return None
        token = self.__auth.upload_token(self.__bucket_name, file_to)
        ret, info = put_file(token, file_to, file_from)
        assert ret['key'] == file_to
        assert ret['hash'] == etag(file_from)
        return info

    def remove(self, file_name):
        if not self.__is_initialized:
            print ("Have not been initialized!")
            return None
        ret, info = self.__bucket.delete(self.__bucket_name, file_name)
        return info

    def list(self):
        pass


class Uploader:
    __type = -1
    TYPE_QINIU = 0
    __uploaders = [QiniuUploader()]
    def _init__(self):
        pass

    def _init_qiniu(self,bucket_name : str, access_key : str, secret_key : str):
        if(self.__uploaders[0].setAuth(access_key,secret_key,bucket_name)):
            self.__type = self.TYPE_QINIU

    def _upload(self, file_from, file_to):
        try:
            self.__uploaders[self.__type].upload(file_from,file_to)
        except IndexError as e:
            print ("You must initilize a uploader before use")


    def _remove(self, file_name):
        try:
            self.__uploaders[self.__type].remove(file_name)
        except IndexError as e:
            print("You must initilize a uploader before use")


    def _list(self):
        try:
            self.__uploaders[self.__type].list()
        except IndexError as e:
            print ("You must initilize a uploader before use")

    def _dispatch(self, method, params):
        return 'bad method'