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


class MagicUploader(FileSystemEventHandler,Uploader):
    def __init__(self):
        FileSystemEventHandler.__init__(self)

    def on_created(self, event):
        absolute_path = self.get_absolute_path(event.src_path)
        related_path = self.get_related_path(absolute_path)
        print("[Created] : %s " % absolute_path)
        if not self.re_check(event.src_path):
            print ("[CHECK] : Ignore file [%s]"%absolute_path)
            return
        if event.is_directory:
            print ("CHECK: Directory Dont Upload")
            return
        _thread.start_new_thread(self._upload,(absolute_path, related_path))

    def on_deleted(self, event):
        absolute_path = self.get_absolute_path(event.src_path)
        related_path = self.get_related_path(absolute_path)
        print("[Deleted] : %s" % absolute_path)
        if not self.re_check(absolute_path):
            print ("[CHECK] : Ignore File [%s]"% absolute_path)
            return
        if event.is_directory:
            print ("[CHECK] : Directory Dont Upload")
            return
        # Do not delete now
        return
        info = self._remove(event.src_path)
        print (info)

    def on_moved(self, event):
        #print ("Move From %s to %s"%(event.src_path[2:],event.dest_path[2:]))
        pass

    def on_modified(self, event):
        #print ("Modified %s"%event.src_path[2:])
        pass

    def re_check(self,file_name : str):
        for item in MagicUploaderConfig.dont_upload:
            p = re.compile(item)
            if p.search(file_name) is not None:
                return False
        return True

    def get_absolute_path(self,file_path):
        return os.path.abspath(file_path)

    def get_related_path(self,file_path):
        if not os.path.isabs(file_path):
            print ("It's not abspath!")
            return None
        return file_path[len(os.path.abspath(MagicUploaderConfig.root_path))+1:]


if __name__ == '__main__':
    event_handler = MagicUploader()
    event_handler._set_do_upload(False)
    event_handler._init_qiniu(MagicUploaderConfig.Qiniu_bucket_name, MagicUploaderConfig.Qiniu_access_key, MagicUploaderConfig.Qiniu_secret_key)
    observer = Observer()
    observer.schedule(event_handler, os.path.abspath(MagicUploaderConfig.root_path), recursive=True)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
