# coding=utf8

import sys
import time
import logging
import re
from watchdog.observers import Observer
from watchdog.events import LoggingEventHandler
from watchdog.events import FileSystemEventHandler
from watchdog.events import FileSystemEvent
from watchdog.events import FileSystemMovedEvent
from uploader import Uploader


class MagicUploader(FileSystemEventHandler,Uploader):
    def __init__(self):
        FileSystemEventHandler.__init__(self)

    def on_created(self, event):
        print("Created: %s" % event.src_path[2:])
        if(event.is_directory)
            return None
        info = self._upload(event.src_path[2:], event.src_path[2:])
        print (info)

    def on_deleted(self, event):
        print("Deleted: %s" % event.src_path[2:])
        if(event.is_directory)
            return None
        info = self._remove(event.src_path[2:])
        print (info)

    def on_moved(self, event):
        print ("Move From %s to %s"%(event.src_path[2:],event.dest_path[2:]))

    def on_modified(self, event):
        print ("Modified %s"%event.src_path[2:])



if __name__ == '__main__':
    access_key = ''
    secret_key = ''
    path = "./"
    event_handler = MagicUploader()
    event_handler._init_qiniu("resources", access_key, secret_key)
    observer = Observer()
    observer.schedule(event_handler, path, recursive=True);
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
