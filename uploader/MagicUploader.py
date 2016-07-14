# coding=utf8

import sys
import time
import logging
import re
import os
from watchdog.observers import Observer
from watchdog.events import LoggingEventHandler
from watchdog.events import FileSystemEventHandler
from watchdog.events import FileSystemEvent
from watchdog.events import FileSystemMovedEvent
from Uploaders import Uploader
from MUConfig import MagicUploaderConfig
from FileStatus import FileStatus
import fcntl
import _thread
from xmlrpc.server import SimpleXMLRPCServer
from xmlrpc.server import SimpleXMLRPCRequestHandler
from xmlrpc.server import SimpleXMLRPCDispatcher
from http.server import SimpleHTTPRequestHandler


def get_absolute_path(file_path : str) -> str:
    return os.path.abspath(file_path)


def get_related_path(file_path : str) -> str:
    if not os.path.isabs(file_path):
        print("It's not abs_path!")
        return None
    return file_path[len(os.path.abspath(MagicUploaderConfig.root_path)) + 1:]

def re_check(file_name: str) -> bool :
    for item in MagicUploaderConfig.dont_upload:
        p = re.compile(item)
        if p.search(file_name) is not None:
            return False
    return True



class MagicUploader(FileSystemEventHandler,Uploader):
    def __init__(self):
        FileSystemEventHandler.__init__(self)

    def upload(self, file_from : str, file_to : str):
        absolute_path = get_absolute_path(file_from)
        related_path = get_related_path(get_absolute_path(file_to))
        _thread.start_new_thread(self._upload,(absolute_path, related_path))

    def on_created(self, event):
        absolute_path = get_absolute_path(event.src_path)
        related_path = get_related_path(absolute_path)
        print("[Created] : %s " % absolute_path)
        if not re_check(event.src_path):
            print ("[CHECK]   : Ignore file [%s]"%absolute_path)
            return
        if event.is_directory:
            print ("[CHECK]   : Directory Dont Upload")
            return
        _thread.start_new_thread(self._upload,(absolute_path, related_path))

    def on_deleted(self, event):
        absolute_path = get_absolute_path(event.src_path)
        related_path = get_related_path(absolute_path)
        print("[Deleted] : %s" % absolute_path)
        if not re_check(absolute_path):
            print ("[CHECK]   : Ignore File [%s]"% absolute_path)
            return
        if event.is_directory:
            print ("[CHECK]   : Directory Dont Upload")
            return
        # Do not delete now
        return
        #info = self._remove(event.src_path)
        #print (info)

    def on_moved(self, event):
        #print ("Move From %s to %s"%(event.src_path[2:],event.dest_path[2:]))
        pass

    def on_modified(self, event):
        #print ("Modified %s"%event.src_path[2:])
        pass


class RequestHandler(SimpleXMLRPCRequestHandler):
#    rpc_paths = ('http://localhost/',)

#    def do_OPTIONS(self):
#        self.send_response(200)
#        self.end_headers()

    # Add these headers to all responses
    def end_headers(self):
        self.send_header("Access-Control-Allow-Headers",
                         "Origin, X-Requested-With, Content-Type, Accept")
        self.send_header("Access-Control-Allow-Origin", "*")
        SimpleXMLRPCRequestHandler.end_headers(self)

#    def do_GET(self):
#        self.send_response(200)
#        self.send_header("Content-type","text/xml")


#    def __dispatch(self,meothd,params):
#        return str(meothd)


def start_xml_rpc(ip : str, port : int, instance : MagicUploader):
    server = SimpleXMLRPCServer((ip, port),allow_none=True, requestHandler=RequestHandler)
    server.register_instance(instance)
    server.register_function(instance.list_files)
    print ("RPC Started")
    server.serve_forever()

if __name__ == '__main__':
    event_handler = MagicUploader()
    event_handler._set_do_upload(True)
    event_handler._init_qiniu(MagicUploaderConfig.Qiniu_bucket_name, MagicUploaderConfig.Qiniu_access_key, MagicUploaderConfig.Qiniu_secret_key)
    event_handler._set_show_process(True)
    observer = Observer()
    observer.schedule(event_handler, os.path.abspath(MagicUploaderConfig.root_path), recursive=False)
    observer.start()
    _thread.start_new_thread(start_xml_rpc,("",8080,event_handler))

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()


